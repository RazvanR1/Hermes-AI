from datetime import datetime, timezone

def ok(data=None, mode=None):
    return {
        "ok": True,
        "mode": mode,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
        "errors": [],
    }

def error(message, mode=None):
    return {
        "ok": False,
        "mode": mode,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": None,
        "errors": [str(message)],
    }
