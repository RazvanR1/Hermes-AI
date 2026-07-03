from datetime import datetime, timezone

def build_inventory():
    inv = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "v6-core-inventory",
        "components": {},
        "summary": {
            "proxmox_vms": 0,
            "proxmox_lxc": 0,
            "docker_containers": 0,
            "docker_running": 0,
            "docker_exited": 0,
            "homeassistant": "unknown",
            "truenas": "unknown",
            "opnsense": "unknown",
        },
        "warnings": [],
    }

    inv["components"]["proxmox"] = _proxmox()
    inv["components"]["docker"] = _docker()
    inv["components"]["homeassistant"] = _homeassistant()
    inv["components"]["truenas"] = _truenas()
    inv["components"]["opnsense"] = _opnsense()

    _fill_summary(inv)
    return inv


def _proxmox():
    try:
        from providers.proxmox import client as proxmox
        resources = proxmox.resources()
        vms, lxcs = [], []
        for item in resources or []:
            if not isinstance(item, dict):
                continue
            kind = str(item.get("type", "")).lower()
            obj = {
                "id": item.get("vmid"),
                "name": item.get("name") or item.get("id") or str(item.get("vmid") or "unknown"),
                "status": item.get("status"),
                "cpu": item.get("cpu"),
                "mem": item.get("mem"),
                "maxmem": item.get("maxmem"),
                "node": item.get("node"),
            }
            if kind == "qemu":
                obj["kind"] = "vm"
                vms.append(obj)
            elif kind == "lxc":
                obj["kind"] = "lxc"
                lxcs.append(obj)
        return {"ok": True, "kind": "virtualization", "vms": vms, "lxcs": lxcs, "counts": {"vms": len(vms), "lxcs": len(lxcs)}}
    except Exception as e:
        return {"ok": False, "kind": "virtualization", "error": str(e), "vms": [], "lxcs": [], "counts": {"vms": 0, "lxcs": 0}}


def _docker():
    try:
        from providers.docker import client as docker
        containers = docker.ps()
        out, running, exited = [], 0, 0
        for item in containers or []:
            if not isinstance(item, dict):
                continue
            status = str(item.get("status") or item.get("State") or "").lower()
            if "up" in status or status == "running":
                running += 1
            elif "exit" in status or "dead" in status or "stop" in status:
                exited += 1
            out.append({
                "name": item.get("name") or item.get("Names") or item.get("container") or item.get("id"),
                "image": item.get("image") or item.get("Image"),
                "status": item.get("status") or item.get("State"),
                "ports": item.get("ports") or item.get("Ports"),
            })
        return {"ok": True, "kind": "containers", "containers": out, "counts": {"total": len(out), "running": running, "exited": exited}}
    except Exception as e:
        return {"ok": False, "kind": "containers", "error": str(e), "containers": [], "counts": {"total": 0, "running": 0, "exited": 0}}


def _homeassistant():
    try:
        from providers.homeassistant import client as ha
        updates = ha.updates()
        available = [u for u in updates or [] if str(u.get("state")).lower() == "on"]
        return {"ok": True, "kind": "automation", "status": "online", "updates_total_entities": len(updates or []), "updates_available": len(available)}
    except Exception as e:
        return {"ok": False, "kind": "automation", "status": "unknown", "error": str(e)}


def _truenas():
    try:
        from providers.truenas import client as truenas
        status = truenas.status() if hasattr(truenas, "status") else None
        return {"ok": True, "kind": "storage", "status": status}
    except Exception as e:
        return {"ok": False, "kind": "storage", "status": "unknown", "error": str(e)}


def _opnsense():
    try:
        from providers.opnsense import client as opnsense
        status = opnsense.summary()
        return {
            "ok": bool(status.get("ok")),
            "kind": "network_firewall",
            "status": "online" if status.get("ok") else "error",
            "version": status.get("product_version"),
            "os_version": status.get("os_version"),
            "updates_available": status.get("updates_count"),
            "needs_reboot": status.get("needs_reboot") or status.get("upgrade_needs_reboot"),
            "repository": status.get("repository"),
        }
    except Exception as e:
        return {"ok": False, "kind": "network_firewall", "status": "unknown", "error": str(e)}


def _fill_summary(inv):
    prox = inv["components"].get("proxmox", {})
    docker = inv["components"].get("docker", {})
    ha = inv["components"].get("homeassistant", {})
    tn = inv["components"].get("truenas", {})
    opn = inv["components"].get("opnsense", {})

    inv["summary"]["proxmox_vms"] = prox.get("counts", {}).get("vms", 0)
    inv["summary"]["proxmox_lxc"] = prox.get("counts", {}).get("lxcs", 0)
    inv["summary"]["docker_containers"] = docker.get("counts", {}).get("total", 0)
    inv["summary"]["docker_running"] = docker.get("counts", {}).get("running", 0)
    inv["summary"]["docker_exited"] = docker.get("counts", {}).get("exited", 0)
    inv["summary"]["homeassistant"] = "online" if ha.get("ok") else "error"
    inv["summary"]["truenas"] = "online" if tn.get("ok") else "error"
    inv["summary"]["opnsense"] = "online" if opn.get("ok") else "error"

    for name, comp in inv["components"].items():
        if not comp.get("ok"):
            inv["warnings"].append(f"{name}: {comp.get('error') or comp.get('status')}")
