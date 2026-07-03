from providers.operations import score as score_mod


def decide(alerts, tasks):
    score = score_mod.calculate(alerts)

    if alerts.get("critical"):
        status = "critical"
    elif alerts.get("warnings"):
        status = "attention_required"
    else:
        status = "ok"

    return {
        "status": status,
        "score": score,
        "critical": alerts.get("critical", []),
        "warnings": alerts.get("warnings", []),
        "info": alerts.get("info", []),
        "healthy": alerts.get("healthy", []),
        "today": tasks,
    }
