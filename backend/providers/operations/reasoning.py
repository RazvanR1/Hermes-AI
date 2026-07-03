def analyze(report):
    status = report.get("status")
    score = report.get("score")
    critical = report.get("critical", []) or []
    warnings = report.get("warnings", []) or []
    today = report.get("today", []) or []

    all_text = " ".join([str(x).lower() for x in critical + warnings])

    storage_problem = any(x in all_text for x in [
        "degraded",
        "smart",
        "uncorrectable",
        "offline",
        "removed",
        "pool",
        "disc",
        "disk",
    ])

    proxmox_updates = _count_updates(warnings, ["proxmox", "debian"])
    ha_updates = _count_updates(warnings, ["home assistant", "ha"])

    health_label = _health_label(score)
    score_bar = _score_bar(score)

    do_now = []
    do_later = []
    can_wait = []
    healthy_notes = []
    blockers = []
    risky_actions = []
    safe_actions = []
    advice = []

    if storage_problem or critical:
        do_now.append({
            "title": "Rezolvă problema TrueNAS / storage",
            "why": "Pool-ul/discul are probleme și acesta este riscul principal pentru date.",
            "risk": "ridicat",
            "estimated_time": "1-2 ore",
        })
        blockers.append("Nu recomand reboot, upgrade major sau mentenanță agresivă până când storage-ul este stabil.")
        risky_actions.extend([
            "Reboot host Proxmox înainte de stabilizarea TrueNAS",
            "Upgrade major TrueNAS/Proxmox cât timp pool-ul este degradat",
        ])
        advice.append("Eu aș rezolva mai întâi storage-ul. Abia după aceea aș face update la Proxmox.")
    else:
        advice.append("Nu văd probleme critice active. Poți face mentenanță normală.")

    if proxmox_updates:
        item = {
            "title": f"Aplică cele {proxmox_updates} update-uri Proxmox/Debian",
            "why": "Menține host-ul actualizat și securizat.",
            "risk": "scăzut",
            "estimated_time": "10-15 min",
        }
        if storage_problem:
            do_later.append(item | {"why": "Sunt utile, dar le-aș face după rezolvarea storage-ului."})
        else:
            do_now.append(item)

    if ha_updates:
        can_wait.append({
            "title": f"Verifică cele {ha_updates} update-uri Home Assistant",
            "why": "Prioritate joasă față de storage și Proxmox.",
            "risk": "scăzut",
            "estimated_time": "5 min",
        })

    if not critical and not warnings:
        healthy_notes.append("Nu sunt probleme sau update-uri importante.")
    else:
        healthy_notes.extend([
            "Proxmox este online" if _contains(report.get("healthy", []), "proxmox") else None,
            "Docker este online" if _contains(report.get("healthy", []), "docker") else None,
            "Home Assistant API este online" if _contains(report.get("healthy", []), "home assistant") else None,
            "TrueNAS răspunde" if _contains(report.get("healthy", []), "truenas") else None,
        ])

    score_explanation = _score_explanation(score, critical, warnings)

    return {
        "version": "v5.2",
        "health_label": health_label,
        "score_bar": score_bar,
        "main_risk": blockers[0] if blockers else None,
        "summary_ro": _summary_ro(score, health_label, storage_problem, critical, warnings),
        "do_now": _dedupe_dicts(do_now),
        "do_later": _dedupe_dicts(do_later),
        "can_wait": _dedupe_dicts(can_wait),
        "healthy_notes": _dedupe([x for x in healthy_notes if x]),
        "score_explanation": score_explanation,
        "advice": _dedupe(advice),
        "blockers": _dedupe(blockers),
        "safe_actions": _dedupe(safe_actions),
        "risky_actions": _dedupe(risky_actions),
        "recommended_order": _recommended_order(today, blockers),
        "response_template_ro": _template_ro(score, health_label, storage_problem, proxmox_updates, ha_updates),
    }


def _template_ro(score, health_label, storage_problem, proxmox_updates, ha_updates):
    if storage_problem:
        headline = "Serverul funcționează, dar nu aș face update-uri până nu rezolvi storage-ul."
        recommendation = "Rezolvă întâi TrueNAS/pool-ul, apoi fă update-urile Proxmox."
    else:
        headline = "Serverul este stabil."
        recommendation = "Poți face update-urile într-o fereastră normală de mentenanță."

    return {
        "headline": headline,
        "format": [
            "🟡 Stare generală",
            "🔥 Fă acum",
            "⏳ După aceea",
            "💤 Poate aștepta",
            "📊 De ce ai acest scor",
            "💡 Recomandarea Hermes",
        ],
        "recommendation": recommendation,
        "style": "Răspunde scurt, în română, ca un administrator senior. Nu repeta aceleași update-uri.",
    }


def _summary_ro(score, health_label, storage_problem, critical, warnings):
    if storage_problem:
        return f"Stare {health_label} ({score}/100). Problema principală este storage-ul TrueNAS."
    if critical:
        return f"Stare {health_label} ({score}/100). Există {len(critical)} problemă critică."
    if warnings:
        return f"Stare {health_label} ({score}/100). Nu sunt probleme critice, dar există mentenanță de făcut."
    return f"Stare bună ({score}/100). Nu sunt probleme importante."


def _score_bar(score):
    if score is None:
        return "necunoscut"
    filled = max(0, min(10, round(score / 10)))
    return "█" * filled + "░" * (10 - filled) + f" {score}%"


def _health_label(score):
    if score is None:
        return "necunoscut"
    if score >= 90:
        return "bună"
    if score >= 75:
        return "acceptabilă, dar necesită atenție"
    if score >= 50:
        return "slabă, necesită intervenție"
    return "critică"


def _score_explanation(score, critical, warnings):
    items = []
    if critical:
        for item in critical:
            low = str(item).lower()
            if any(x in low for x in ["degraded", "smart", "uncorrectable", "offline", "removed", "pool"]):
                items.append({"impact": "-15", "reason": "Problemă TrueNAS/storage"})
            else:
                items.append({"impact": "-15", "reason": str(item)})
    if warnings:
        for item in warnings:
            low = str(item).lower()
            if "proxmox" in low or "debian" in low:
                items.append({"impact": "-4", "reason": "Update-uri Proxmox/Debian disponibile"})
            elif "home assistant" in low:
                items.append({"impact": "-4", "reason": "Update-uri Home Assistant disponibile"})
            else:
                items.append({"impact": "-4", "reason": str(item)})
    if not items:
        items.append({"impact": "0", "reason": "Nu sunt probleme active"})
    return {
        "score": score,
        "bar": _score_bar(score),
        "items": _dedupe_dicts(items),
    }


def _recommended_order(tasks, blockers):
    if not tasks:
        return []
    order = []
    for t in tasks:
        title = t.get("title", "")
        component = t.get("component", "")
        priority = t.get("priority", "")
        order.append({
            "priority": priority,
            "component": component,
            "title": title,
            "why": _why(component, title, blockers),
            "estimated_time": t.get("estimated_time"),
            "risk": t.get("risk"),
        })
    return order


def _why(component, title, blockers):
    c = str(component).lower()
    t = str(title).lower()
    if "truenas" in c or "disc" in t or "disk" in t or "smart" in t or "pool" in t:
        return "Protejează datele și reduce riscul de pierdere a pool-ului."
    if "proxmox" in c:
        if blockers:
            return "Este util, dar nu este prioritar cât timp storage-ul are probleme."
        return "Menține host-ul actualizat și securizat."
    if "home assistant" in c:
        return "Update minor, prioritate joasă."
    return "Task de mentenanță recomandat."


def _count_updates(warnings, keywords):
    total = 0
    for warning in warnings or []:
        text = str(warning).lower()
        if any(k in text for k in keywords):
            number = _first_int(text)
            total += number if number else 1
    return total


def _first_int(text):
    current = ""
    for ch in text:
        if ch.isdigit():
            current += ch
        elif current:
            return int(current)
    return int(current) if current else 0


def _contains(items, needle):
    needle = needle.lower()
    return any(needle in str(x).lower() for x in items or [])


def _dedupe(items):
    out = []
    seen = set()
    for item in items:
        if not item:
            continue
        key = str(item)
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def _dedupe_dicts(items):
    out = []
    seen = set()
    for item in items:
        key = tuple(sorted((item or {}).items()))
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out
