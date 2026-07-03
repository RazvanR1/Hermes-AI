def _norm_text(text):
    return " ".join(str(text or "").lower().split())


def dedupe(items):
    out, seen = [], set()
    for item in items or []:
        if not item:
            continue
        key = _norm_text(item)
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def _add_update_warning(warnings, component, count):
    try:
        count = int(count or 0)
    except Exception:
        count = 0
    if count <= 0:
        return
    if component == "proxmox":
        warnings.append(f"{count} Proxmox/Debian updates available")
    elif component == "homeassistant":
        warnings.append(f"{count} Home Assistant update available")


def collect(dashboard_result, updates_result):
    critical, warnings, info, healthy = [], [], [], []

    prox_updates_seen = False
    ha_updates_seen = False

    if dashboard_result.get("ok"):
        dashboard = dashboard_result["data"]

        for alert in dashboard.get("alerts", []):
            msg = str(alert)
            low = msg.lower()

            if "rest api" in low:
                continue

            # Avoid duplicated update alerts from both dashboard() and update_status().
            if "proxmox" in low and "update" in low:
                prox_updates_seen = True
                continue
            if "home assistant" in low and "update" in low:
                ha_updates_seen = True
                continue

            if any(x in low for x in ["uncorrectable", "degraded", "offline", "smart"]):
                critical.append(msg)
            else:
                warnings.append(msg)

        health = dashboard.get("health", {})
        if health.get("proxmox"):
            healthy.append("Proxmox online")
        if health.get("docker"):
            healthy.append("Docker online")
        if health.get("homeassistant"):
            healthy.append("Home Assistant API online")
        if health.get("truenas"):
            healthy.append("TrueNAS online")
    else:
        critical.append(f"Dashboard failed: {dashboard_result.get('error')}")

    if updates_result.get("ok"):
        updates = updates_result["data"]
        summary = updates.get("summary", {})

        prox = summary.get("proxmox_updates_count") or 0
        ha = summary.get("homeassistant_updates_count") or 0

        _add_update_warning(warnings, "proxmox", prox)
        _add_update_warning(warnings, "homeassistant", ha)

        tn = updates.get("truenas", {})
        if tn.get("error"):
            info.append("TrueNAS update check unavailable via REST API")
    else:
        warnings.append(f"Update check failed: {updates_result.get('error')}")

    return {
        "critical": dedupe(critical),
        "warnings": dedupe(warnings),
        "info": dedupe(info),
        "healthy": dedupe(healthy),
    }
