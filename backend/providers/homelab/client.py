from providers.proxmox import client as proxmox
from providers.docker import client as docker
from providers.homeassistant import client as ha
from providers.truenas import client as truenas

def health():
    return {
        "proxmox": proxmox.status(),
        "docker": docker.ps(),
        "homeassistant": {
            "status": ha.status(),
        },
        "truenas": truenas.health(),
    }

def health_summary():
    p = proxmox.status()
    d = docker.ps()
    h = ha.status()
    t = truenas.health_summary()

    proxmox_running = [x for x in p if x.get("status") == "running"]
    docker_running = [x for x in d if x.get("state") == "running"]
    docker_exited = [x for x in d if x.get("state") != "running"]

    tn_pools = t.get("pools", [])
    tn_alerts = t.get("alerts", [])

    critical_alerts = []
    for a in tn_alerts:
        msg = (a.get("formatted") or "").lower()

        # ignorăm warning-ul de migrare REST API TrueNAS
        if "rest api" in msg:
            continue

        level = str(a.get("level", "")).upper()
        if level in ["CRITICAL", "ERROR", "WARNING"]:
            critical_alerts.append(a)

    pool_summary = []
    for pool in tn_pools:
        pool_summary.append({
            "name": pool.get("name"),
            "status": pool.get("status"),
            "healthy": pool.get("healthy"),
            "warning": pool.get("warning"),
            "scan_function": (pool.get("scan") or {}).get("function"),
            "scan_state": (pool.get("scan") or {}).get("state"),
            "scan_percentage": (pool.get("scan") or {}).get("percentage"),
        })

    score = 100

    score -= len(docker_exited) * 5
    score -= len(critical_alerts) * 10

    for pool in pool_summary:
        if pool.get("status") != "ONLINE":
            score -= 30
        if pool.get("healthy") is False:
            score -= 30

    score = max(score, 0)

    return {
        "overall": "attention_required" if critical_alerts or docker_exited or score < 100 else "ok",
        "score": score,
        "proxmox": {
            "total": len(p),
            "running": len(proxmox_running),
            "not_running": [x.get("name") for x in p if x.get("status") != "running"],
            "top_cpu": sorted(
                [
                    {
                        "name": x.get("name"),
                        "vmid": x.get("vmid"),
                        "cpu_percent": x.get("cpu_percent"),
                        "ram_gb": x.get("ram_gb"),
                        "max_ram_gb": x.get("max_ram_gb"),
                    }
                    for x in p
                ],
                key=lambda x: x.get("cpu_percent") or 0,
                reverse=True
            )[:5],
        },
        "docker": {
            "total": len(d),
            "running": len(docker_running),
            "exited": [
                {
                    "name": x.get("name"),
                    "status": x.get("status"),
                }
                for x in docker_exited
            ],
        },
        "homeassistant": h,
        "truenas": {
            "system": t.get("system"),
            "pools": pool_summary,
            "important_alerts": critical_alerts,
        },
    }

def auto_fix():
    report = {
        "fixed": [],
        "manual_required": [],
        "checked": [],
        "errors": [],
    }

    try:
        summary = health_summary()
        report["checked"].append("homelab_health_summary")
    except Exception as e:
        report["errors"].append({
            "component": "homelab_health_summary",
            "error": str(e),
        })
        return report

    # Docker: start exited containers
    for c in summary.get("docker", {}).get("exited", []):
        name = c.get("name")
        status = c.get("status")

        if not name:
            continue

        try:
            logs = docker.logs(name, 40)
        except Exception as e:
            logs = f"Could not read logs: {e}"

        try:
            result = docker.start(name)
            report["fixed"].append({
                "component": "docker",
                "container": name,
                "previous_status": status,
                "action": "start",
                "result": result,
                "recent_logs": logs[-2000:],
            })
        except Exception as e:
            report["errors"].append({
                "component": "docker",
                "container": name,
                "action": "start",
                "error": str(e),
                "recent_logs": logs[-2000:],
            })

    # TrueNAS: report only, no automatic destructive action
    truenas_data = summary.get("truenas", {})
    for pool in truenas_data.get("pools", []):
        if pool.get("status") not in ["ONLINE", None] or pool.get("healthy") is False:
            report["manual_required"].append({
                "component": "truenas",
                "type": "pool",
                "name": pool.get("name"),
                "status": pool.get("status"),
                "healthy": pool.get("healthy"),
                "warning": pool.get("warning"),
            })

    for alert in truenas_data.get("important_alerts", []):
        formatted = alert.get("formatted") or ""
        if "REST API" in formatted:
            continue
        report["manual_required"].append({
            "component": "truenas",
            "type": "alert",
            "level": alert.get("level"),
            "klass": alert.get("klass"),
            "message": formatted,
        })

    return report
