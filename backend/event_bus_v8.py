from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List
import json
import uuid

try:
    from notifications.hub import notify
except Exception:
    notify = None

DATA_DIR = Path(__file__).resolve().parent / "data"
EVENTS_FILE = DATA_DIR / "events_v8.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_store() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not EVENTS_FILE.exists():
        EVENTS_FILE.write_text("[]", encoding="utf-8")


def load_events(limit: int | None = None) -> List[Dict[str, Any]]:
    _ensure_store()
    try:
        raw = EVENTS_FILE.read_text(encoding="utf-8").strip()
        events = json.loads(raw or "[]")
        if not isinstance(events, list):
            events = []
    except Exception:
        events = []

    if limit:
        return events[:limit]
    return events


def save_events(events: List[Dict[str, Any]]) -> None:
    _ensure_store()
    tmp = EVENTS_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(events, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(EVENTS_FILE)


def emit_event(
    event_type: str,
    mission_id: str | None = None,
    step_id: str | None = None,
    level: str = "info",
    message: str = "",
    data: Dict[str, Any] | None = None,
    source: str = "hermes",
) -> Dict[str, Any]:
    event = {
        "event_id": str(uuid.uuid4()),
        "time": _now(),
        "type": event_type,
        "level": level,
        "mission_id": mission_id,
        "step_id": step_id,
        "message": message,
        "data": data or {},
        "source": source,
    }

    events = load_events()
    events.insert(0, event)
    events = events[:5000]
    save_events(events)

    notification_result = None
    if notify is not None:
        try:
            notification_result = notify(event)
        except Exception as exc:
            notification_result = {"ok": False, "error": str(exc)}

    if notification_result is not None:
        event["notification"] = notification_result

    return event


def events_for_mission(mission_id: str, limit: int = 200) -> List[Dict[str, Any]]:
    return [
        event for event in load_events()
        if event.get("mission_id") == mission_id
    ][:limit]


def clear_events() -> Dict[str, Any]:
    save_events([])
    return {"ok": True, "cleared": True}
