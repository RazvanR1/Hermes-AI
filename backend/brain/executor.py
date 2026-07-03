def execute(plan: dict, ctx: dict):
    results = {}

    for step in plan.get("steps", []):
        name = step.get("name")
        source = step.get("source")

        if source == "inventory":
            results[name] = ctx.get("inventory")
        elif source == "graph":
            results[name] = ctx.get("graph")
        elif source == "guardian":
            results[name] = ctx.get("guardian")
        elif source == "incidents":
            results[name] = ctx.get("incidents")
        elif source == "history":
            results[name] = ctx.get("history")
        elif source == "actions":
            try:
                from core import actions
                results[name] = actions.plan(plan.get("request", ""))
            except Exception as e:
                results[name] = {"error": str(e)}
        elif source == "reasoning":
            try:
                from core import reasoning
                results[name] = reasoning.analyze({
                    "inventory": ctx.get("inventory"),
                    "incidents": {"open": (ctx.get("incidents") or {}).get("open", [])},
                    "score": None,
                })
            except Exception as e:
                results[name] = {"error": str(e)}

    return {"mode": "brain_result_v1", "plan": plan, "results": results, "context_errors": ctx.get("errors", [])}
