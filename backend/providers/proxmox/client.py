import requests
import urllib3
from core.config import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ALIASES = {
    "homeassistant": 100,
    "ha": 100,
    "zigbee": 101,
    "zigbee2mqtt": 101,
    "truenas": 103,
    "portainer-vm": 102,
    "portainer": 200,
    "docker": 200,
    "ollama": 201,
    "hermes": 202,
    "hermesagent": 202,
}

def node():
    return config.get("PROXMOX_NODE", "proxmox")

def env(name):
    return config.require(name)

def auth_header():
    return {
        "Authorization": (
            f"PVEAPIToken={env('PROXMOX_USER')}!"
            f"{env('PROXMOX_TOKEN_NAME')}={env('PROXMOX_TOKEN_VALUE')}"
        )
    }

def api(method, path, data=None):
    url = f"{env('PROXMOX_HOST').rstrip('/')}/api2/json{path}"
    kwargs = {"headers": auth_header(), "verify": False, "timeout": 15}
    if method.upper() == "GET":
        kwargs["params"] = data
    else:
        kwargs["data"] = data
    r = requests.request(method, url, **kwargs)
    r.raise_for_status()
    return r.json().get("data")

def resolve(target):
    if isinstance(target, int):
        return target
    t = str(target).strip()
    if t.isdigit():
        return int(t)
    if t in ALIASES:
        return ALIASES[t]
    raise RuntimeError(f"Nu cunosc serviciul: {target}")

def vm_type(vmid):
    resources_data = api("GET", "/cluster/resources")
    for item in resources_data:
        if item.get("vmid") == int(vmid):
            if item.get("type") == "qemu":
                return "qemu"
            if item.get("type") == "lxc":
                return "lxc"
    raise RuntimeError(f"Nu găsesc VMID: {vmid}")

def status():
    data = api("GET", "/cluster/resources")
    out = []
    for item in data:
        if item.get("type") in ["qemu", "lxc"]:
            out.append({
                "type": item.get("type"),
                "vmid": item.get("vmid"),
                "name": item.get("name"),
                "status": item.get("status"),
                "cpu_percent": round(item.get("cpu", 0) * 100, 1),
                "ram_gb": round(item.get("mem", 0) / 1024 / 1024 / 1024, 2),
                "max_ram_gb": round(item.get("maxmem", 0) / 1024 / 1024 / 1024, 2),
            })
    return out

def storage():
    data = api("GET", "/cluster/resources")
    out = []
    for item in data:
        if item.get("type") == "storage":
            total = item.get("maxdisk", 0)
            used = item.get("disk", 0)
            out.append({
                "storage": item.get("storage"),
                "status": item.get("status"),
                "used_gb": round(used / 1024 / 1024 / 1024, 1),
                "total_gb": round(total / 1024 / 1024 / 1024, 1),
            })
    return out

def power(action, target):
    vmid = resolve(target)
    kind = vm_type(vmid)
    return api("POST", f"/nodes/{node()}/{kind}/{vmid}/status/{action}")

def snapshot(target, snapshot_name):
    vmid = resolve(target)
    kind = vm_type(vmid)
    return api("POST", f"/nodes/{node()}/{kind}/{vmid}/snapshot", data={"snapname": snapshot_name})

def snapshots(target):
    vmid = resolve(target)
    kind = vm_type(vmid)
    return api("GET", f"/nodes/{node()}/{kind}/{vmid}/snapshot")

def delete_snapshot(target, snapshot_name):
    vmid = resolve(target)
    kind = vm_type(vmid)
    return api("DELETE", f"/nodes/{node()}/{kind}/{vmid}/snapshot/{snapshot_name}")

def tasks(limit=20):
    data = api("GET", f"/nodes/{node()}/tasks")
    try:
        limit = int(limit)
    except Exception:
        limit = 20
    return data[:limit]

def task_status(upid):
    return api("GET", f"/nodes/{node()}/tasks/{upid}/status")

def node_status():
    return api("GET", f"/nodes/{node()}/status")

def version():
    return api("GET", "/version")

def cluster_status():
    return api("GET", "/cluster/status")

def resources():
    return api("GET", "/cluster/resources")

def vm_config(target):
    vmid = resolve(target)
    kind = vm_type(vmid)
    return api("GET", f"/nodes/{node()}/{kind}/{vmid}/config")

def storage_content(storage="local"):
    return api("GET", f"/nodes/{node()}/storage/{storage}/content")

def updates():
    try:
        result = api("GET", f"/nodes/{node()}/apt/update")
    except Exception:
        result = []
    try:
        versions = api("GET", f"/nodes/{node()}/version")
    except Exception:
        versions = {}
    return {
        "updates": result,
        "updates_count": len(result) if isinstance(result, list) else 0,
        "version": versions,
    }
