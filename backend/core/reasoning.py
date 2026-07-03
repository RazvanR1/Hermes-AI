def analyze(context):
    """
    Hermes Next Reasoning v1.

    Input:
      - rendered sysadmin report
      - inventory
      - incidents
      - core_plan

    Output:
      structured conclusions that the LLM should explain, not invent.
    """
    score = context.get("score") or context.get("health_score")
    incidents = _open_incidents(context)
    inventory = context.get("inventory", {}) or {}

    critical = [i for i in incidents if i.get("severity") == "critical"]
    warnings = [i for i in incidents if i.get("severity") == "warning"]

    storage_incidents = [
        i for i in incidents
        if i.get("provider") == "truenas"
        or _contains(i.get("title"), ["pool", "storage", "smart", "disk", "disc", "degraded", "removed"])
    ]

    proxmox_updates = _count_matching(incidents, ["proxmox", "debian", "updates"])
    ha_updates = _count_matching(incidents, ["home assistant", "homeassistant", "update"])
    opnsense = _opnsense_summary(inventory)

    block_updates = bool(storage_incidents)

    conclusions = {
        "version": "reasoning_v1",
        "score": score,
        "health_label": _health_label(score),
        "main_risk": None,
        "priority": [],
        "blockers": [],
        "recommended_actions": [],
        "safe_to_do": [],
        "wait_until": [],
        "providers": {
            "opnsense": opnsense,
        },
        "counts": {
            "open_incidents": len(incidents),
            "critical": len(critical),
            "warnings": len(warnings),
            "proxmox_update_incidents": proxmox_updates,
            "homeassistant_update_incidents": ha_updates,
        },
        "llm_instructions": [
            "Răspunde în română.",
            "Nu inventa detalii care nu sunt în JSON.",
            "Menționează riscul principal primul.",
            "Dacă storage-ul este degradat, recomandă să NU se facă reboot/update major.",
            "Folosește secțiuni scurte: Stare, Fă acum, După aceea, Evită.",
        ],
    }

    if storage_incidents:
        main = storage_incidents[0]
        conclusions["main_risk"] = _clean_html(main.get("title"))
        conclusions["priority"].append({
            "level": 1,
            "provider": "truenas",
            "title": "Rezolvă storage-ul TrueNAS",
            "reason": _clean_html(main.get("title")),
            "risk": "ridicat",
        })
        conclusions["blockers"].append({
            "type": "storage_degraded",
            "message": "Nu recomand reboot, upgrade major sau mentenanță agresivă până când storage-ul este stabil.",
        })
        conclusions["recommended_actions"].extend([
            "Verifică în TrueNAS discul/pool-ul afectat.",
            "Înlocuiește sau reintegrează discul marcat ca REMOVED dacă este cazul.",
            "Așteaptă ca pool-ul să revină ONLINE înainte de update-uri majore.",
        ])
        conclusions["wait_until"].append("TrueNAS pool ONLINE / storage stabil")

    if proxmox_updates:
        action = "Aplică update-urile Proxmox/Debian într-o fereastră de mentenanță."
        if block_updates:
            action = "Amână update-urile Proxmox/Debian până după stabilizarea TrueNAS."
        conclusions["recommended_actions"].append(action)

    if ha_updates:
        conclusions["safe_to_do"].append("Verifică update-urile Home Assistant din UI; prioritate joasă față de storage.")

    if opnsense.get("status") == "online":
        if opnsense.get("updates_available", 0):
            conclusions["recommended_actions"].append("Verifică update-urile OPNsense.")
        else:
            conclusions["safe_to_do"].append("OPNsense este online și nu raportează update-uri disponibile.")

    if not conclusions["main_risk"]:
        if critical:
            conclusions["main_risk"] = _clean_html(critical[0].get("title"))
        elif warnings:
            conclusions["main_risk"] = _clean_html(warnings[0].get("title"))
        else:
            conclusions["main_risk"] = "Nu există incidente critice active."

    return conclusions


def _open_incidents(context):
    if isinstance(context.get("incidents"), dict):
        return context["incidents"].get("open", []) or []
    return context.get("open_incidents", []) or []


def _contains(text, words):
    t = str(text or "").lower()
    return any(w in t for w in words)


def _count_matching(incidents, words):
    count = 0
    for incident in incidents:
        title = str(incident.get("title") or "").lower()
        provider = str(incident.get("provider") or "").lower()
        text = provider + " " + title
        if any(w in text for w in words):
            count += 1
    return count


def _opnsense_summary(inventory):
    comp = (inventory.get("components") or {}).get("opnsense") or {}
    return {
        "status": comp.get("status"),
        "version": comp.get("version"),
        "updates_available": comp.get("updates_available") or 0,
        "needs_reboot": bool(comp.get("needs_reboot")),
        "repository": comp.get("repository"),
    }


def _health_label(score):
    try:
        s = int(score)
    except Exception:
        return "necunoscut"
    if s >= 90:
        return "bun"
    if s >= 75:
        return "acceptabil, dar necesită atenție"
    if s >= 50:
        return "problematic"
    return "critic"


def _clean_html(text):
    text = str(text or "")
    return (
        text.replace("<br>", " ")
            .replace("<ul>", " ")
            .replace("</ul>", " ")
            .replace("<li>", " - ")
            .replace("</li>", " ")
    )
