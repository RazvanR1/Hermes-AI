from datetime import datetime, timezone

def build():
    from brain import context
    from core import recommendations
    from core import taskqueue

    ctx = context.build()
    inv = ctx.get("inventory") or {}
    summary = inv.get("summary") or {}

    recs = recommendations.build(ctx).get("items", [])
    tasks = taskqueue.list_tasks(10)

    opnsense_reboot = any(
        (r.get("provider") == "opnsense" and "reboot" in str(r.get("title", "")).lower())
        for r in recs
    )

    incidents = ((ctx.get("incidents") or {}).get("open")) or []

    score = 100
    score -= min(len(incidents) * 8, 30)
    if opnsense_reboot:
        score -= 8
    if summary.get("docker_exited", 0) > 0:
        score -= 20

    score = max(score, 0)

    providers = [
        {
            "name": "Docker",
            "status": "healthy" if summary.get("docker_exited", 0) == 0 else "warning",
            "primary": f"{summary.get('docker_running', 0)}/{summary.get('docker_containers', 0)} running",
            "secondary": f"{summary.get('docker_exited', 0)} exited",
        },
        {
            "name": "Proxmox",
            "status": "healthy",
            "primary": f"{summary.get('proxmox_vms', 0)} VM",
            "secondary": f"{summary.get('proxmox_lxc', 0)} LXC",
        },
        {
            "name": "TrueNAS",
            "status": summary.get("truenas", "unknown"),
            "primary": str(summary.get("truenas", "unknown")),
            "secondary": "storage provider",
        },
        {
            "name": "OPNsense",
            "status": "warning" if opnsense_reboot else summary.get("opnsense", "unknown"),
            "primary": "reboot pending" if opnsense_reboot else str(summary.get("opnsense", "unknown")),
            "secondary": "firewall/router",
        },
        {
            "name": "Home Assistant",
            "status": summary.get("homeassistant", "unknown"),
            "primary": str(summary.get("homeassistant", "unknown")),
            "secondary": "automation hub",
        },
    ]

    timeline = [
        {
            "time": datetime.now(timezone.utc).isoformat(),
            "title": "Dashboard refreshed",
            "description": "Mission Control loaded latest Hermes state.",
            "type": "info",
        },
        {
            "time": datetime.now(timezone.utc).isoformat(),
            "title": "Guardian active",
            "description": f"{len(incidents)} open incidents detected.",
            "type": "success" if len(incidents) == 0 else "warning",
        },
    ]

    return {
        "mode": "dashboard_v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "health": {
            "score": score,
            "status": "healthy" if score >= 90 else "warning" if score >= 70 else "critical",
            "open_incidents": len(incidents),
        },
        "providers": providers,
        "recommendations": recs[:5],
        "tasks": tasks[:5],
        "timeline": timeline,
    }
