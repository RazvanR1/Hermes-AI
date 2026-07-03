#!/usr/bin/env python3
import os
import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NODE = "proxmox"

ALIASES = {
    "homeassistant": 100,
    "ha": 100,
    "zigbee": 101,
    "zigbee2mqtt": 101,
    "truenas": 103,
    "portainer": 200,
    "docker": 200,
    "ollama": 201,
    "hermes": 202,
    "hermesagent": 202,
}

def _env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Lipsește variabila {name}")
    return value

def auth_header():
    return {
        "Authorization": (
            f"PVEAPIToken={_env('PROXMOX_USER')}!"
            f"{_env('PROXMOX_TOKEN_NAME')}={_env('PROXMOX_TOKEN_VALUE')}"
        )
    }

def api(method: str, path: str, data=None):
    host = _env("PROXMOX_HOST")
    url = f"{host}/api2/json{path}"
    r = requests.request(
        method,
        url,
        headers=auth_header(),
        data=data,
        verify=False,
        timeout=20,
    )
    r.raise_for_status()
    return r.json().get("data")

def resolve(target):
    target = str(target)
    if target.isdigit():
        return int(target)

    key = target.lower()
    if key in ALIASES:
        return ALIASES[key]

    raise RuntimeError(f"Nu cunosc serviciul: {target}")

def vm_type(vmid):
    resources = api("GET", "/cluster/resources")
    for item in resources:
        if item.get("vmid") == vmid:
            return item["type"], item.get("name", str(vmid)), item.get("status", "-")

    raise RuntimeError(f"Nu găsesc VM/LXC cu ID {vmid}")

def status():
    resources = api("GET", "/cluster/resources")
    result = []

    for item in resources:
        if item.get("type") in ["qemu", "lxc"]:
            result.append({
                "type": item.get("type"),
                "vmid": item.get("vmid"),
                "name": item.get("name"),
                "status": item.get("status"),
                "cpu_percent": round(item.get("cpu", 0) * 100, 1),
                "ram_gb": round(item.get("mem", 0) / 1024 / 1024 / 1024, 2),
                "max_ram_gb": round(item.get("maxmem", 0) / 1024 / 1024 / 1024, 2),
            })

    return result

def storage():
    resources = api("GET", "/cluster/resources")
    result = []

    for item in resources:
        if item.get("type") == "storage":
            used = round(item.get("disk", 0) / 1024 / 1024 / 1024, 1)
            total = round(item.get("maxdisk", 0) / 1024 / 1024 / 1024, 1)
            result.append({
                "storage": item.get("storage"),
                "status": item.get("status"),
                "used_gb": used,
                "total_gb": total,
            })

    return result

def power(action: str, target):
    vmid = resolve(target)
    typ, name, current_status = vm_type(vmid)
    api_type = "qemu" if typ == "qemu" else "lxc"

    if action == "start":
        endpoint = f"/nodes/{NODE}/{api_type}/{vmid}/status/start"
    elif action == "stop":
        endpoint = f"/nodes/{NODE}/{api_type}/{vmid}/status/stop"
    elif action == "shutdown":
        endpoint = f"/nodes/{NODE}/{api_type}/{vmid}/status/shutdown"
    elif action == "restart":
        if api_type == "qemu":
            endpoint = f"/nodes/{NODE}/{api_type}/{vmid}/status/reboot"
        else:
            endpoint = f"/nodes/{NODE}/{api_type}/{vmid}/status/restart"
    else:
        raise RuntimeError(f"Comandă necunoscută: {action}")

    task = api("POST", endpoint)

    return {
        "action": action,
        "type": typ,
        "vmid": vmid,
        "name": name,
        "previous_status": current_status,
        "task": task,
    }

def snapshot(target, name=None):
    vmid = resolve(target)
    typ, vm_name, current_status = vm_type(vmid)
    api_type = "qemu" if typ == "qemu" else "lxc"

    if not name:
        name = f"hermes-{int(time.time())}"

    task = api(
        "POST",
        f"/nodes/{NODE}/{api_type}/{vmid}/snapshot",
        data={
            "snapname": name,
            "description": "Created by Hermes HomeLab Plugin",
        },
    )

    return {
        "type": typ,
        "vmid": vmid,
        "name": vm_name,
        "snapshot": name,
        "task": task,
    }

def snapshots(target):
    vmid = resolve(target)

    try:
        return api("GET", f"/nodes/{NODE}/qemu/{vmid}/snapshot")
    except Exception:
        return api("GET", f"/nodes/{NODE}/lxc/{vmid}/snapshot")

def delete_snapshot(target, snapshot_name):
    vmid = resolve(target)

    try:
        return api(
            "DELETE",
            f"/nodes/{NODE}/qemu/{vmid}/snapshot/{snapshot_name}"
        )
    except Exception:
        return api(
            "DELETE",
            f"/nodes/{NODE}/lxc/{vmid}/snapshot/{snapshot_name}"
        )

def tasks(limit=20):
    data = api("GET", f"/nodes/{NODE}/tasks")
    try:
        limit = int(limit)
    except Exception:
        limit = 20
    return data[:limit]

def node_status():
    return api("GET", f"/nodes/{NODE}/status")

def version():
    return api("GET", "/version")

def cluster_status():
    return api("GET", "/cluster/status")

def resources():
    return api("GET", "/cluster/resources")

def vm_config(target):
    vmid = resolve(target)

    try:
        return api("GET", f"/nodes/{NODE}/qemu/{vmid}/config")
    except Exception:
        return api("GET", f"/nodes/{NODE}/lxc/{vmid}/config")

def task_status(upid):
    return api("GET", f"/nodes/{NODE}/tasks/{upid}/status")

def storage_content(storage="local"):
    return api("GET", f"/nodes/{NODE}/storage/{storage}/content")

def node_status():
    return api("GET", f"/nodes/{NODE}/status")

def version():
    return api("GET", "/version")

def cluster_status():
    return api("GET", "/cluster/status")

def resources():
    return api("GET", "/cluster/resources")

def vm_config(target):
    vmid = resolve(target)

    try:
        return api("GET", f"/nodes/{NODE}/qemu/{vmid}/config")
    except Exception:
        return api("GET", f"/nodes/{NODE}/lxc/{vmid}/config")

def task_status(upid):
    return api("GET", f"/nodes/{NODE}/tasks/{upid}/status")

def storage_content(storage="local"):
    return api("GET", f"/nodes/{NODE}/storage/{storage}/content")

def node_status():
    return api("GET", f"/nodes/{NODE}/status")

def version():
    return api("GET", "/version")

def cluster_status():
    return api("GET", "/cluster/status")

def resources():
    return api("GET", "/cluster/resources")

def vm_config(target):
    vmid = resolve(target)

    try:
        return api("GET", f"/nodes/{NODE}/qemu/{vmid}/config")
    except Exception:
        return api("GET", f"/nodes/{NODE}/lxc/{vmid}/config")

def task_status(upid):
    return api("GET", f"/nodes/{NODE}/tasks/{upid}/status")

def storage_content(storage="local"):
    return api("GET", f"/nodes/{NODE}/storage/{storage}/content")

def node_status():
    return api("GET", f"/nodes/{NODE}/status")

def version():
    return api("GET", "/version")

def cluster_status():
    return api("GET", "/cluster/status")

def resources():
    return api("GET", "/cluster/resources")

def vm_config(target):
    vmid = resolve(target)

    try:
        return api("GET", f"/nodes/{NODE}/qemu/{vmid}/config")
    except Exception:
        return api("GET", f"/nodes/{NODE}/lxc/{vmid}/config")

def task_status(upid):
    return api("GET", f"/nodes/{NODE}/tasks/{upid}/status")

def storage_content(storage="local"):
    return api("GET", f"/nodes/{NODE}/storage/{storage}/content")

def node_status():
    return api("GET", f"/nodes/{NODE}/status")

def version():
    return api("GET", "/version")

def cluster_status():
    return api("GET", "/cluster/status")

def resources():
    return api("GET", "/cluster/resources")

def vm_config(target):
    vmid = resolve(target)

    try:
        return api("GET", f"/nodes/{NODE}/qemu/{vmid}/config")
    except Exception:
        return api("GET", f"/nodes/{NODE}/lxc/{vmid}/config")

def task_status(upid):
    return api("GET", f"/nodes/{NODE}/tasks/{upid}/status")

def storage_content(storage="local"):
    return api("GET", f"/nodes/{NODE}/storage/{storage}/content")
