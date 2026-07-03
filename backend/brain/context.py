def build():
    ctx = {"inventory": None, "graph": None, "guardian": None, "incidents": None, "history": None, "errors": []}

    try:
        from core import inventory as inventory_core
        ctx["inventory"] = inventory_core.build_inventory()
    except Exception as e:
        ctx["errors"].append(f"inventory: {e}")

    try:
        from core.relationships import build_from_inventory
        if ctx["inventory"]:
            ctx["graph"] = build_from_inventory(ctx["inventory"]).to_dict()
    except Exception as e:
        ctx["errors"].append(f"graph: {e}")

    try:
        from core import guardian
        ctx["guardian"] = guardian.status()
    except Exception as e:
        ctx["errors"].append(f"guardian: {e}")

    try:
        from core import incidents
        ctx["incidents"] = {
            "stats": incidents.stats(),
            "open": incidents.list_open(),
            "closed": incidents.list_closed(20),
        }
    except Exception as e:
        ctx["errors"].append(f"incidents: {e}")

    try:
        from providers.operations import history
        ctx["history"] = {"stats": history.stats(), "latest": history.latest(10)}
    except Exception as e:
        ctx["errors"].append(f"history: {e}")

    return ctx
