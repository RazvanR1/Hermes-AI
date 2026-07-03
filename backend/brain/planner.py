def build_plan(request: str, routing: dict, ctx: dict):
    intent = routing.get("intent", "health")
    q = (request or "").lower()
    steps = []

    if "guardian" in q:
        steps.append({"name": "guardian.status", "source": "guardian"})
    elif any(x in q for x in ["depinde", "impact", "afecteaza", "afectează"]):
        steps.append({"name": "graph.impact", "source": "graph"})
    elif intent == "inventory":
        steps.append({"name": "inventory.summary", "source": "inventory"})
        steps.append({"name": "graph.summary", "source": "graph"})
    elif intent == "incidents":
        steps.append({"name": "incidents.open", "source": "incidents"})
        steps.append({"name": "reasoning.priorities", "source": "reasoning"})
    elif intent == "memory":
        steps.append({"name": "history.latest", "source": "history"})
    elif intent == "actions":
        steps.append({"name": "actions.plan", "source": "actions"})
    else:
        steps.extend([
            {"name": "guardian.status", "source": "guardian"},
            {"name": "incidents.open", "source": "incidents"},
            {"name": "inventory.summary", "source": "inventory"},
            {"name": "reasoning.health", "source": "reasoning"},
        ])

    return {"mode": "brain_plan_v1", "request": request, "intent": intent, "routing": routing, "steps": steps}
