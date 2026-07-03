def status():
    try:
        from core import guardian
        state = guardian.status().get("last_run") or {}
    except Exception as e:
        return {"mode": "autonomy_status_v1", "ok": False, "error": str(e)}

    return {
        "mode": "autonomy_status_v1",
        "ok": state.get("ok"),
        "timestamp": state.get("timestamp"),
        "errors": state.get("errors", []),
        "autoheal": state.get("autoheal"),
        "actions": state.get("actions", []),
        "open_incidents": (state.get("incidents") or {}).get("stats", {}).get("open"),
    }
