def render(report, request=""):
    decision = report.get("decision", {})
    reasoning = report.get("reasoning", {})

    return {
        "mode": "sysadmin_v5.2",
        "request": request,

        "summary": report.get("summary", {}),
        "status": decision.get("status"),
        "score": decision.get("score"),
        "health_label": reasoning.get("health_label"),
        "score_bar": reasoning.get("score_bar"),

        "summary_ro": reasoning.get("summary_ro"),
        "main_risk": reasoning.get("main_risk"),

        "sections": {
            "stare_generala": {
                "label": reasoning.get("health_label"),
                "score": decision.get("score"),
                "score_bar": reasoning.get("score_bar"),
                "summary": reasoning.get("summary_ro"),
            },
            "fa_acum": reasoning.get("do_now", []),
            "dupa_aceea": reasoning.get("do_later", []),
            "poate_astepta": reasoning.get("can_wait", []),
            "sanatos": reasoning.get("healthy_notes", []),
            "scor_explicat": reasoning.get("score_explanation", {}),
            "recomandarea_hermes": reasoning.get("advice", []),
            "evita": reasoning.get("risky_actions", []),
        },

        "critical": decision.get("critical", []),
        "warnings": decision.get("warnings", []),
        "healthy": decision.get("healthy", []),
        "info": decision.get("info", []),
        "today": decision.get("today", []),

        "reasoning": reasoning,
        "predictions": report.get("trend", {}).get("predictions", []),
        "changes": report.get("trend", {}).get("changes", []),
        "raw": report.get("raw", {}),
    }
