import os
import requests
from typing import Dict, Any
from .base import Tool

class ProxmoxTool(Tool):
    name = "proxmox"

    def __init__(self):
        self.url = os.getenv("PROXMOX_URL", "").rstrip("/")
        self.token_id = os.getenv("PROXMOX_TOKEN_ID", "")
        self.token_secret = os.getenv("PROXMOX_TOKEN_SECRET", "")
        self.verify_ssl = os.getenv("PROXMOX_VERIFY_SSL", "false").lower() == "true"

    def _headers(self):
        return {
            "Authorization": f"PVEAPIToken={self.token_id}={self.token_secret}"
        }

    def _get(self, path: str) -> Dict[str, Any]:
        if not self.url or not self.token_id or not self.token_secret:
            return {
                "ok": False,
                "error": "Proxmox credentials not configured."
            }

        try:
            r = requests.get(
                f"{self.url}/api2/json{path}",
                headers=self._headers(),
                verify=self.verify_ssl,
                timeout=10,
            )
            return {
                "ok": r.ok,
                "status_code": r.status_code,
                "data": r.json().get("data") if r.headers.get("content-type", "").startswith("application/json") else None,
                "error": "" if r.ok else r.text,
            }
        except Exception as e:
            return {
                "ok": False,
                "error": str(e)
            }

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        if action == "version":
            return self._get("/version")

        if action == "nodes":
            return self._get("/nodes")

        if action == "vms":
            nodes = self._get("/nodes")
            if not nodes.get("ok"):
                return nodes

            result = []

            for node in nodes.get("data", []):
                node_name = node.get("node")
                qemu = self._get(f"/nodes/{node_name}/qemu")
                lxc = self._get(f"/nodes/{node_name}/lxc")

                result.append({
                    "node": node_name,
                    "qemu": qemu.get("data", []),
                    "lxc": lxc.get("data", []),
                })

            return {
                "ok": True,
                "data": result
            }

        return {
            "ok": False,
            "error": f"Unknown Proxmox action '{action}'"
        }

proxmox_tool = ProxmoxTool()
