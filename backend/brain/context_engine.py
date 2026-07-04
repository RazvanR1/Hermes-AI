from brain import dashboard
from brain import session

def build(session_id: str = "default"):
    data = dashboard.build()

    return {
        "mode": "context_v1",
        "dashboard": data,
        "health": data.get("health", {}),
        "providers": data.get("providers", []),
        "recommendations": data.get("recommendations", []),
        "tasks": data.get("tasks", []),
        "timeline": data.get("timeline", []),
        "conversation": session.history(session_id),
    }
