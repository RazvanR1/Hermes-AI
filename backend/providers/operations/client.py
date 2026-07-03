from providers.homelab import client as homelab
from providers.proxmox import client as proxmox
from providers.truenas import client as truenas
from providers.homeassistant import client as ha
from providers.docker import client as docker

try:
    from providers.opnsense import client as opnsense
except Exception:
    opnsense = None


def overview():
    summary = homelab.health_summary()
    score = summary.get("score", 0)

    if score >= 95:
        status = "excellent"
    elif score >= 80:
        status = "good"
    elif score >= 60:
        status = "warning"
    else:
        status = "critical"

    return {
        "status": status,
        "score": score,
        "overall": summary.get("overall"),
        "recommendation": {
            "excellent": "Everything looks healthy.",
            "good": "Minor issues detected.",
            "warning": "Administrator attention recommended.",
            "critical": "Immediate intervention required.",
        }[status],
        "proxmox": summary.get("proxmox"),
        "docker": summary.get("docker"),
        "homeassistant": summary.get("homeassistant"),
        "truenas": summary.get("truenas"),
    }


def opnsense_status():
    if opnsense is None:
        return {
            "ok": False,
            "component": "opnsense",
            "error": "OPNsense provider not available",
        }
    return opnsense.summary()


def update_status():
    prox = proxmox.updates()
    tn = truenas.update_status()
    ha_updates = ha.updates()
    opn = opnsense_status()

    ha_available = [
        u for u in ha_updates
        if str(u.get("state")).lower() == "on"
    ]

    opn_updates = 0
    opn_reboot = False

    if opn.get("ok"):
        opn_updates = opn.get("updates_count") or 0
        opn_reboot = bool(opn.get("needs_reboot") or opn.get("upgrade_needs_reboot"))

    return {
        "proxmox": prox,
        "truenas": tn,
        "opnsense": opn,
        "homeassistant": {
            "total_update_entities": len(ha_updates),
            "updates_available": ha_available,
        },
        "docker": {
            "note": "Docker image freshness check not implemented yet. Current containers can be listed with docker_ps.",
            "containers": docker.ps(),
        },
        "summary": {
            "proxmox_updates_count": prox.get("updates_count"),
            "homeassistant_updates_count": len(ha_available),
            "truenas_update_check": "ok" if not tn.get("error") else "error",
            "opnsense_updates_count": opn_updates,
            "opnsense_needs_reboot": opn_reboot,
            "opnsense_status": "ok" if opn.get("ok") else "error",
        },
    }


def dashboard():
    health = overview()
    updates = update_status()
    opn = updates.get("opnsense", {}) or {}

    alerts = []
    recommendations = []

    prox_updates = updates.get("summary", {}).get("proxmox_updates_count") or 0
    ha_updates = updates.get("summary", {}).get("homeassistant_updates_count") or 0
    opn_updates = updates.get("summary", {}).get("opnsense_updates_count") or 0
    opn_needs_reboot = updates.get("summary", {}).get("opnsense_needs_reboot") or False

    docker_exited = (
        health.get("docker", {}) or {}
    ).get("exited", [])

    truenas_alerts = (
        health.get("truenas", {}) or {}
    ).get("important_alerts", [])

    if prox_updates:
        alerts.append(f"{prox_updates} Proxmox updates available")
        recommendations.append("Update Proxmox packages when you have a maintenance window")

    if ha_updates:
        alerts.append(f"{ha_updates} Home Assistant update entities available")
        recommendations.append("Review Home Assistant updates in the HA UI")

    if opn.get("ok"):
        if opn_updates:
            alerts.append(f"{opn_updates} OPNsense updates available")
            recommendations.append("Review OPNsense firmware updates")
        if opn_needs_reboot:
            alerts.append("OPNsense requires reboot")
            recommendations.append("Schedule an OPNsense reboot after checking active network usage")
    else:
        alerts.append(f"OPNsense check failed: {opn.get('error')}")
        recommendations.append("Verify OPNsense API credentials and network connectivity")

    if docker_exited:
        alerts.append(f"{len(docker_exited)} Docker containers are not running")
        recommendations.append("Run homelab_auto_fix or inspect Docker logs")

    for alert in truenas_alerts:
        msg = alert.get("formatted") or ""
        if "REST API" in msg:
            continue
        alerts.append(msg)
        recommendations.append("Review TrueNAS alert")

    status = "ok"
    if alerts:
        status = "attention_required"

    return {
        "status": status,
        "health_score": health.get("score"),
        "health": {
            "overall": health.get("overall"),
            "proxmox": health.get("proxmox"),
            "docker": health.get("docker"),
            "homeassistant": health.get("homeassistant"),
            "truenas": health.get("truenas"),
            "opnsense": opn,
        },
        "updates": {
            "proxmox_updates": prox_updates,
            "homeassistant_updates": ha_updates,
            "opnsense_updates": opn_updates,
            "opnsense_needs_reboot": opn_needs_reboot,
            "truenas": updates.get("truenas"),
        },
        "alerts": alerts,
        "recommendations": recommendations,
    }
