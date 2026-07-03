def build(decision):
    return {
        "headline": f"Homelab score {decision.get('score')}/100",
        "status": decision.get("status"),
        "critical_count": len(decision.get("critical", [])),
        "warning_count": len(decision.get("warnings", [])),
        "task_count": len(decision.get("today", [])),
    }
