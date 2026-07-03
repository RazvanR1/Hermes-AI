from providers.operations import client

def plan():
    dashboard = client.dashboard()

    tasks = []

    if dashboard["updates"]["proxmox_updates"] > 0:
        tasks.append({
            "priority": "medium",
            "component": "Proxmox",
            "title": f'{dashboard["updates"]["proxmox_updates"]} updates available',
            "risk": "low",
            "estimated_time": "10-15 min",
        })

    if dashboard["updates"]["homeassistant_updates"] > 0:
        tasks.append({
            "priority": "low",
            "component": "Home Assistant",
            "title": f'{dashboard["updates"]["homeassistant_updates"]} updates available',
            "risk": "low",
            "estimated_time": "5 min",
        })

    for alert in dashboard["alerts"]:
        if "uncorrectable" in alert.lower():
            tasks.append({
                "priority": "critical",
                "component": "TrueNAS",
                "title": "Replace failing disk",
                "risk": "high",
                "estimated_time": "1-2 hours",
            })

    priority = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    tasks.sort(key=lambda x: priority[x["priority"]])

    return {
        "status": dashboard["status"],
        "score": dashboard["health_score"],
        "tasks": tasks,
    }
