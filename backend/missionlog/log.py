from datetime import datetime
from typing import Dict, List

_events: List[Dict] = []

def push(agent: str, message: str, status: str = "info"):
    _events.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "agent": agent,
        "status": status,
        "message": message,
    })

    if len(_events) > 200:
        del _events[:-200]

def get():
    return list(_events)

def clear():
    _events.clear()
