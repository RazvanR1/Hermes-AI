from collections import defaultdict
from datetime import datetime

_sessions = defaultdict(list)
MAX_MESSAGES = 20

def add(session_id: str, role: str, text: str):
    _sessions[session_id].append({
        "role": role,
        "text": text,
        "timestamp": datetime.utcnow().isoformat()
    })

    if len(_sessions[session_id]) > MAX_MESSAGES:
        _sessions[session_id] = _sessions[session_id][-MAX_MESSAGES:]

def history(session_id: str):
    return _sessions.get(session_id, [])

def clear(session_id: str):
    _sessions.pop(session_id, None)

def stats():
    return {
        "sessions": len(_sessions),
        "messages": sum(len(v) for v in _sessions.values())
    }
