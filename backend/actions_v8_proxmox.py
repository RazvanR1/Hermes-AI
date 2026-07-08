import os
from typing import Dict, Any
import requests

from actions_v8_registry import Action, register


def _env(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


class HermesProxmoxClient:
    def __init__(self):
        self.base_url = _env("PROXMOX_URL", "PROXMOX_API_URL", "PVE_URL").rstrip("/")
        self.token_id = _env("PROXMOX_TOKEN_ID", "PVE_TOKEN_ID")
        self.token_secret = _env("PROXMOX_TOKEN_SECRET", "PVE_TOKEN_SECRET")
        self.verify_ssl = _env("PROXMOX_VERIFY_SSL", "PVE_VERIFY_SSL", default="false").lower() == "true"

        if not self.base_url:
            raise RuntimeError("Missing PROXMOX_URL / PROXMOX_API_URL / PVE_URL")
        if not self.token_id:
            raise RuntimeError("Missing PROXMOX_TOKEN_ID / PVE_TOKEN_ID")
        if not self.token_secret:
            raise RuntimeError("Missing PROXMOX_TOKEN_SECRET / PVE_TOKEN_SECRET")

    def _headers(self):
        return {
            "Authorization": f"PVEAPIToken={self.token_id}={self.token_secret}"
        }

    def _url(self, path: str) -> str:
        path = path if path.startswith("/") else f"/{path}"
        if path.startswith("/api2/json"):
            return f"{self.base_url}{path}"
        return f"{self.base_url}/api2/json{path}"

    def get(self, path: str) -> Any:
        r = requests.get(
            self._url(path),
            headers=self._headers(),
            verify=self.verify_ssl,
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("data", data)

    def post(self, path: str, payload: dict | None = None) -> Any:
        r = requests.post(
            self._url(path),
            headers=self._headers(),
            json=payload or {},
            verify=self.verify_ssl,
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("data", data)


def _client():
    return HermesProxmoxClient()


def _require(params: dict, key: str):
    value = params.get(key)
    if value in (None, ""):
        raise ValueError(f"Missing required param: {key}")
    return value


def proxmox_nodes(params: dict) -> Dict[str, Any]:
    client = _client()
    data = client.get("/nodes")
    return {
        "ok": True,
        "data": data,
    }


def proxmox_vm_status(params: dict) -> Dict[str, Any]:
    node = _require(params, "node")
    vmid = _require(params, "vmid")
    client = _client()
    data = client.get(f"/nodes/{node}/qemu/{vmid}/status/current")
    return {
        "ok": True,
        "node": node,
        "vmid": vmid,
        "data": data,
    }


def proxmox_lxc_status(params: dict) -> Dict[str, Any]:
    node = _require(params, "node")
    vmid = _require(params, "vmid")
    client = _client()
    data = client.get(f"/nodes/{node}/lxc/{vmid}/status/current")
    return {
        "ok": True,
        "node": node,
        "vmid": vmid,
        "data": data,
    }


def _post_qemu_status(action: str, params: dict) -> Dict[str, Any]:
    node = _require(params, "node")
    vmid = _require(params, "vmid")
    client = _client()
    data = client.post(f"/nodes/{node}/qemu/{vmid}/status/{action}")
    return {
        "ok": True,
        "node": node,
        "vmid": vmid,
        "action": action,
        "data": data,
    }


def _post_lxc_status(action: str, params: dict) -> Dict[str, Any]:
    node = _require(params, "node")
    vmid = _require(params, "vmid")
    client = _client()
    data = client.post(f"/nodes/{node}/lxc/{vmid}/status/{action}")
    return {
        "ok": True,
        "node": node,
        "vmid": vmid,
        "action": action,
        "data": data,
    }


def vm_start(params: dict) -> Dict[str, Any]:
    return _post_qemu_status("start", params)


def vm_shutdown(params: dict) -> Dict[str, Any]:
    return _post_qemu_status("shutdown", params)


def vm_reboot(params: dict) -> Dict[str, Any]:
    return _post_qemu_status("reboot", params)


def vm_reset(params: dict) -> Dict[str, Any]:
    return _post_qemu_status("reset", params)


def vm_stop(params: dict) -> Dict[str, Any]:
    return _post_qemu_status("stop", params)


def lxc_start(params: dict) -> Dict[str, Any]:
    return _post_lxc_status("start", params)


def lxc_shutdown(params: dict) -> Dict[str, Any]:
    return _post_lxc_status("shutdown", params)


def lxc_reboot(params: dict) -> Dict[str, Any]:
    return _post_lxc_status("reboot", params)


def lxc_stop(params: dict) -> Dict[str, Any]:
    return _post_lxc_status("stop", params)


def register_proxmox_actions() -> None:
    register(Action("proxmox.nodes", "SAFE", "List Proxmox nodes", proxmox_nodes))
    register(Action("proxmox.vm.status", "SAFE", "Get Proxmox VM status", proxmox_vm_status))
    register(Action("proxmox.lxc.status", "SAFE", "Get Proxmox LXC status", proxmox_lxc_status))

    register(Action("proxmox.vm.start", "CONFIRM", "Start Proxmox VM", vm_start))
    register(Action("proxmox.vm.shutdown", "CONFIRM", "Gracefully shutdown Proxmox VM", vm_shutdown))
    register(Action("proxmox.vm.reboot", "CONFIRM", "Gracefully reboot Proxmox VM", vm_reboot))
    register(Action("proxmox.vm.reset", "CONFIRM", "Force reset Proxmox VM", vm_reset))
    register(Action("proxmox.vm.stop", "CONFIRM", "Force stop Proxmox VM", vm_stop))

    register(Action("proxmox.lxc.start", "CONFIRM", "Start Proxmox LXC", lxc_start))
    register(Action("proxmox.lxc.shutdown", "CONFIRM", "Gracefully shutdown Proxmox LXC", lxc_shutdown))
    register(Action("proxmox.lxc.reboot", "CONFIRM", "Reboot Proxmox LXC", lxc_reboot))
    register(Action("proxmox.lxc.stop", "CONFIRM", "Force stop Proxmox LXC", lxc_stop))


register_proxmox_actions()
