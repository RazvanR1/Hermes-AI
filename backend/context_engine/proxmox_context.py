from __future__ import annotations

from collections.abc import Callable
from typing import Any

from actions_v8_proxmox import HermesProxmoxClient

from .models import GuestType, ProxmoxGuestContext


ClientFactory = Callable[[], HermesProxmoxClient]


class ProxmoxContextProvider:
    def __init__(
        self,
        client_factory: ClientFactory | None = None,
    ) -> None:
        self._client_factory = client_factory or HermesProxmoxClient

    def get_guest(
        self,
        vmid: int,
        guest_type: GuestType | str | None = None,
        node: str | None = None,
    ) -> ProxmoxGuestContext:
        normalized_type = self._normalize_guest_type(guest_type)

        context = ProxmoxGuestContext(
            vmid=int(vmid),
            guest_type=normalized_type or GuestType.VM,
        )

        try:
            client = self._client_factory()
        except Exception as exc:
            context.warnings.append(
                f"Clientul Proxmox nu a putut fi inițializat: {exc}"
            )
            return context

        resource = self._find_resource(
            client=client,
            vmid=int(vmid),
            guest_type=normalized_type,
            node=node,
            warnings=context.warnings,
        )

        if resource is None:
            context.warnings.append(
                f"Nu a fost găsită o resursă Proxmox cu VMID {vmid}."
            )
            return context

        detected_type = self._resource_guest_type(resource)

        if detected_type is None:
            context.warnings.append(
                f"Tipul resursei VMID {vmid} nu a putut fi determinat."
            )
            return context

        context.guest_type = detected_type
        context.exists = True
        context.node = str(resource.get("node") or node or "") or None
        context.name = self._optional_string(
            resource.get("name")
            or resource.get("template")
        )
        context.status = str(resource.get("status") or "unknown")
        context.running = context.status.lower() == "running"

        if not context.node:
            context.warnings.append(
                f"Nodul pentru VMID {vmid} nu a putut fi determinat."
            )
            return context

        endpoint_type = (
            "qemu"
            if context.guest_type is GuestType.VM
            else "lxc"
        )

        status = self._safe_get(
            client,
            (
                f"/nodes/{context.node}/{endpoint_type}/"
                f"{context.vmid}/status/current"
            ),
            context.warnings,
            "statusul curent",
        )

        config = self._safe_get(
            client,
            (
                f"/nodes/{context.node}/{endpoint_type}/"
                f"{context.vmid}/config"
            ),
            context.warnings,
            "configurația",
        )

        snapshots = self._safe_get(
            client,
            (
                f"/nodes/{context.node}/{endpoint_type}/"
                f"{context.vmid}/snapshot"
            ),
            context.warnings,
            "snapshot-urile",
            default=[],
        )

        running_backup_tasks = self._safe_get(
            client,
            (
                f"/nodes/{context.node}/tasks"
                "?typefilter=vzdump&limit=500"
            ),
            context.warnings,
            "task-urile de backup",
            default=[],
        )

        self._apply_status(context, status)
        self._apply_config(context, config)
        self._apply_snapshots(context, snapshots)

        context.backup_running = self._backup_targets_guest(
            running_backup_tasks,
            context.vmid,
        )

        return context

    @staticmethod
    def _normalize_guest_type(
        guest_type: GuestType | str | None,
    ) -> GuestType | None:
        if guest_type is None:
            return None

        if isinstance(guest_type, GuestType):
            return guest_type

        normalized = str(guest_type).strip().lower()

        if normalized in {"vm", "qemu"}:
            return GuestType.VM

        if normalized in {"lxc", "ct", "container"}:
            return GuestType.LXC

        raise ValueError(
            f"Tip de guest Proxmox necunoscut: {guest_type}"
        )

    def _find_resource(
        self,
        *,
        client: HermesProxmoxClient,
        vmid: int,
        guest_type: GuestType | None,
        node: str | None,
        warnings: list[str],
    ) -> dict[str, Any] | None:
        resources = self._safe_get(
            client,
            "/cluster/resources?type=vm",
            warnings,
            "inventarul clusterului",
            default=[],
        )

        if not isinstance(resources, list):
            warnings.append(
                "Inventarul Proxmox nu are formatul așteptat."
            )
            return None

        for resource in resources:
            try:
                resource_vmid = int(resource.get("vmid"))
            except (TypeError, ValueError):
                continue

            if resource_vmid != vmid:
                continue

            detected_type = self._resource_guest_type(resource)

            if guest_type and detected_type is not guest_type:
                continue

            if node and str(resource.get("node")) != node:
                continue

            return resource

        return None

    @staticmethod
    def _resource_guest_type(
        resource: dict[str, Any],
    ) -> GuestType | None:
        resource_type = str(
            resource.get("type")
            or resource.get("kind")
            or ""
        ).lower()

        if resource_type in {"qemu", "vm"}:
            return GuestType.VM

        if resource_type in {"lxc", "ct", "container"}:
            return GuestType.LXC

        return None

    @staticmethod
    def _safe_get(
        client: HermesProxmoxClient,
        path: str,
        warnings: list[str],
        description: str,
        default: Any = None,
    ) -> Any:
        try:
            result = client.get(path)
            return default if result is None else result
        except Exception as exc:
            warnings.append(
                f"Nu am putut citi {description}: {exc}"
            )
            return default

    @staticmethod
    def _apply_status(
        context: ProxmoxGuestContext,
        status: Any,
    ) -> None:
        if not isinstance(status, dict):
            return

        context.raw_status = status

        context.status = str(
            status.get("status")
            or context.status
            or "unknown"
        )
        context.running = context.status.lower() == "running"

        context.cpu_usage = ProxmoxContextProvider._optional_float(
            status.get("cpu")
        )
        context.memory_used_bytes = (
            ProxmoxContextProvider._optional_int(
                status.get("mem")
            )
        )
        context.memory_total_bytes = (
            ProxmoxContextProvider._optional_int(
                status.get("maxmem")
            )
        )
        context.uptime_seconds = (
            ProxmoxContextProvider._optional_int(
                status.get("uptime")
            )
        )

        if (
            context.memory_used_bytes is not None
            and context.memory_total_bytes
            and context.memory_total_bytes > 0
        ):
            context.memory_usage_percent = round(
                (
                    context.memory_used_bytes
                    / context.memory_total_bytes
                )
                * 100,
                2,
            )

        status_lock = status.get("lock")

        if status_lock:
            context.locked = True
            context.lock_reason = str(status_lock)

    @staticmethod
    def _apply_config(
        context: ProxmoxGuestContext,
        config: Any,
    ) -> None:
        if not isinstance(config, dict):
            return

        if config.get("name"):
            context.name = str(config["name"])

        config_lock = config.get("lock")

        if config_lock:
            context.locked = True
            context.lock_reason = str(config_lock)

        raw_tags = config.get("tags")

        if isinstance(raw_tags, str):
            context.tags = [
                tag.strip()
                for tag in raw_tags.replace(",", ";").split(";")
                if tag.strip()
            ]

    @staticmethod
    def _apply_snapshots(
        context: ProxmoxGuestContext,
        snapshots: Any,
    ) -> None:
        if not isinstance(snapshots, list):
            return

        context.snapshot_count = sum(
            1
            for snapshot in snapshots
            if str(snapshot.get("name") or "").lower()
            != "current"
        )

    @staticmethod
    def _backup_targets_guest(
        tasks: Any,
        vmid: int,
    ) -> bool:
        if not isinstance(tasks, list):
            return False

        expected = str(vmid)

        for task in tasks:
            if not isinstance(task, dict):
                continue

            task_id = str(task.get("id") or "")
            upid = str(task.get("upid") or "")
            task_type = str(task.get("type") or "").lower()
            status = str(task.get("status") or "running").lower()

            if task_type and task_type != "vzdump":
                continue

            if status not in {"running", ""}:
                continue

            if (
                task_id == expected
                or f":{expected}:" in upid
                or f":{expected}/" in upid
            ):
                return True

        return False

    @staticmethod
    def _optional_int(value: Any) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _optional_float(value: Any) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _optional_string(value: Any) -> str | None:
        if value in (None, ""):
            return None
        return str(value)


proxmox_context_provider = ProxmoxContextProvider()
