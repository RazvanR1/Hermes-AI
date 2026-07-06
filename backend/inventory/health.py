from inventory.inventory import inventory

def calculate_health():
    data = inventory.collect()

    if not data.get("ok"):
        return {
            "score": 0,
            "status": "offline",
            "incidents": 1,
        }

    summary = data["inventory"]["summary"]

    total = summary["running"] + summary["stopped"]

    score = 100 if total == 0 else round(summary["running"] / total * 100)

    incidents = summary["stopped"]

    if score >= 95:
        status = "healthy"
    elif score >= 80:
        status = "warning"
    else:
        status = "critical"

    return {
        "score": score,
        "status": status,
        "incidents": incidents,
        "summary": summary,
    }
