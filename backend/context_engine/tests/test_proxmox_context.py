from __future__ import annotations

import unittest
from typing import Any

from context_engine import (
    GuestType,
    ProxmoxContextProvider,
)


class FakeProxmoxClient:
    def __init__(
        self,
        responses: dict[str, Any],
    ) -> None:
        self.responses = responses

    def get(self, path: str) -> Any:
        if path not in self.responses:
            raise RuntimeError(
                f"Răspuns fake lipsă pentru: {path}"
            )

        response = self.responses[path]

        if isinstance(response, Exception):
            raise response

        return response


class ProxmoxContextProviderTests(unittest.TestCase):
    def test_running_vm_context(self) -> None:
        responses = {
            "/cluster/resources?type=vm": [
                {
                    "vmid": 110,
                    "node": "proxmox",
                    "type": "qemu",
                    "name": "Docker",
                    "status": "running",
                }
            ],
            (
                "/nodes/proxmox/qemu/110/"
                "status/current"
            ): {
                "status": "running",
                "cpu": 0.15,
                "mem": 4_000_000_000,
                "maxmem": 8_000_000_000,
                "uptime": 3600,
            },
            "/nodes/proxmox/qemu/110/config": {
                "name": "Docker",
                "tags": "production;docker",
            },
            "/nodes/proxmox/qemu/110/snapshot": [
                {"name": "current"},
                {"name": "before-update"},
            ],
            (
                "/nodes/proxmox/tasks"
                "?typefilter=vzdump&limit=500"
            ): [],
        }

        provider = ProxmoxContextProvider(
            client_factory=lambda: FakeProxmoxClient(
                responses
            )
        )

        context = provider.get_guest(
            110,
            GuestType.VM,
        )

        self.assertTrue(context.exists)
        self.assertTrue(context.running)
        self.assertEqual(context.node, "proxmox")
        self.assertEqual(context.name, "Docker")
        self.assertEqual(context.snapshot_count, 1)
        self.assertFalse(context.backup_running)
        self.assertEqual(
            context.memory_usage_percent,
            50.0,
        )
        self.assertEqual(
            context.tags,
            ["production", "docker"],
        )

    def test_locked_vm(self) -> None:
        responses = {
            "/cluster/resources?type=vm": [
                {
                    "vmid": 110,
                    "node": "proxmox",
                    "type": "qemu",
                    "status": "running",
                }
            ],
            (
                "/nodes/proxmox/qemu/110/"
                "status/current"
            ): {
                "status": "running",
            },
            "/nodes/proxmox/qemu/110/config": {
                "lock": "backup",
            },
            "/nodes/proxmox/qemu/110/snapshot": [],
            (
                "/nodes/proxmox/tasks"
                "?typefilter=vzdump&limit=500"
            ): [
                {
                    "id": "110",
                    "type": "vzdump",
                    "status": "running",
                }
            ],
        }

        provider = ProxmoxContextProvider(
            client_factory=lambda: FakeProxmoxClient(
                responses
            )
        )

        context = provider.get_guest(110)

        self.assertTrue(context.exists)
        self.assertTrue(context.locked)
        self.assertEqual(
            context.lock_reason,
            "backup",
        )
        self.assertTrue(context.backup_running)

    def test_missing_guest(self) -> None:
        provider = ProxmoxContextProvider(
            client_factory=lambda: FakeProxmoxClient(
                {
                    "/cluster/resources?type=vm": []
                }
            )
        )

        context = provider.get_guest(999)

        self.assertFalse(context.exists)
        self.assertFalse(context.running)
        self.assertTrue(context.warnings)

    def test_api_failure_is_reported(self) -> None:
        provider = ProxmoxContextProvider(
            client_factory=lambda: FakeProxmoxClient(
                {
                    "/cluster/resources?type=vm": (
                        RuntimeError("API unavailable")
                    )
                }
            )
        )

        context = provider.get_guest(110)

        self.assertFalse(context.exists)
        self.assertTrue(
            any(
                "API unavailable" in warning
                for warning in context.warnings
            )
        )


if __name__ == "__main__":
    unittest.main()
