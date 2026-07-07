import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

DATA_FILE = Path("data/missions.json")


def _ensure_file():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]")


def _read() -> List[Dict[str, Any]]:
    _ensure_file()
    return json.loads(DATA_FILE.read_text())


def _write(items: List[Dict[str, Any]]):
    _ensure_file()
    DATA_FILE.write_text(json.dumps(items[-500:], indent=2))


def add(mission: str, status: str, executed: Dict[str, Any]) -> Dict[str, Any]:
    items = _read()

    item = {
        "id": str(uuid.uuid4()),
        "time": datetime.now(timezone.utc).isoformat(),
        "mission": mission,
        "status": status,
        "ok": executed.get("ok", False),
        "steps": executed.get("steps", []),
    }

    items.append(item)
    _write(items)

    return item


def list_all(limit: int = 100) -> List[Dict[str, Any]]:
    return list(reversed(_read()))[:limit]


def get(mission_id: str) -> Optional[Dict[str, Any]]:
    for item in _read():
        if item.get("id") == mission_id:
            return item
    return None


def clear():
    _write([])
