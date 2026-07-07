import os
from typing import Dict, Any
import requests

from .base import Tool


class ProxmoxActions(Tool):
    name = "proxmox_action"

    def __init__(self):
        self.url = os.getenv("PROXMOX_URL", "").rstrip("/")
        self.token_id = os.getenv("PROXMOX_TOKEN_ID", "")
        self.token_secret = os.getenv("PROXMOX_TOKEN_SECRET", "")
        self.verify = os.getenv("PROXMOX_VERIFY_SSL", "false").lower() == "true"

    def headers(self):
        return {
            "Authorization": f"PVEAPIToken={self.token_id}={self.token_secret}"
        }

    def post(self, path: str) -> Dict[str, Any]:
        if not self.url or not self.token_id or not self.token_secret:
            return {"ok": False, "error": "Proxmox credentials not configured."}

        r = requests.post(
            self.url + "/api2/json" + path,
            headers=self.headers(),
            verify=self.verify,
            timeout=20,
        )

        return {
            "ok": r.ok,
            "status_code": r.status_code,
            "data": r.json().get("data") if r.headers.get("content-type", "").startswith("application/json") else None,
            "error": "" if r.ok else r.text,
        }

    def execute(self, action: str, **params) -> Dict[str, Any]:
        node = params.get("node")
        vmid = params.get("vmid")

        if not node or not vmid:
            return {"ok": False, "error": "Missing node or vmid."}

        actions = {
            "start": "start",
            "shutdown": "shutdown",
            "stop": "stop",
            "reboot": "reboot",
            "reset": "reset",
        }

        if action not in actions:
            return {"ok": False, "error": f"Unknown action '{action}'."}

        return self.post(f"/nodes/{node}/qemu/{vmid}/status/{actions[action]}")


proxmox_actions = ProxmoxActions()
