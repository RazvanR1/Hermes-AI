def summarize(result: dict):
    plan = result.get("plan", {})
    results = result.get("results", {})
    ctx_errors = result.get("context_errors", [])

    incidents_payload = results.get("incidents.open") or {}
    open_incidents = incidents_payload.get("open", []) if isinstance(incidents_payload, dict) else []

    inventory = results.get("inventory.summary") or {}
    graph = results.get("graph.summary") or {}
    guardian = results.get("guardian.status") or {}
    reasoning = results.get("reasoning.health") or results.get("reasoning.priorities") or {}

    return {
        "mode": "brain_answer_v1",
        "request": plan.get("request"),
        "intent": plan.get("intent"),
        "plan": plan,
        "summary": {
            "open_incidents": len(open_incidents),
            "inventory_summary": inventory.get("summary") if isinstance(inventory, dict) else None,
            "graph_counts": graph.get("counts") if isinstance(graph, dict) else None,
            "guardian_last_ok": ((guardian.get("last_run") or {}).get("ok") if isinstance(guardian, dict) else None),
            "main_risk": reasoning.get("main_risk") if isinstance(reasoning, dict) else None,
            "errors": ctx_errors,
        },
        "data": results,
    }
