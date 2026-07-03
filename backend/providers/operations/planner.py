def plan(alerts):
    tasks = []

    for item in alerts.get("critical", []):
        low = item.lower()
        if any(x in low for x in ["smart", "uncorrectable", "disk", "sdd"]):
            tasks.append({
                "priority": "critical",
                "component": "TrueNAS",
                "title": "Verifică și pregătește înlocuirea discului cu erori SMART",
                "risk": "high",
                "estimated_time": "1-2 ore",
            })

    for item in alerts.get("warnings", []):
        low = item.lower()
        if "proxmox" in low or "debian" in low:
            tasks.append({
                "priority": "medium",
                "component": "Proxmox",
                "title": "Aplică update-urile Proxmox/Debian",
                "risk": "low",
                "estimated_time": "10-15 min",
            })
        if "home assistant" in low:
            tasks.append({
                "priority": "low",
                "component": "Home Assistant",
                "title": "Verifică update-ul disponibil în Home Assistant",
                "risk": "low",
                "estimated_time": "5 min",
            })

    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    tasks.sort(key=lambda x: order.get(x.get("priority"), 99))

    out, seen = [], set()
    for t in tasks:
        key = (t.get("component"), t.get("title"))
        if key not in seen:
            seen.add(key)
            out.append(t)
    return out
