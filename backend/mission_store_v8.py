from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json

DATA_DIR = Path(__file__).resolve().parent / "data"
MISSION_FILE = DATA_DIR / "missions_v8.json"

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _ensure_store() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not MISSION_FILE.exists():
        MISSION_FILE.write_text("[]", encoding="utf-8")

def load_missions() -> List[Dict[str, Any]]:
    _ensure_store()
    try:
        return json.loads(MISSION_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_missions(missions: List[Dict[str, Any]]) -> None:
    _ensure_store()
    MISSION_FILE.write_text(json.dumps(missions, indent=2, ensure_ascii=False), encoding="utf-8")

def save_mission(mission: Dict[str, Any]) -> Dict[str, Any]:
    missions = load_missions()
    mission["updated_at"] = _now()
    missions.insert(0, mission)
    save_missions(missions)
    return mission

def update_mission(mission: Dict[str, Any]) -> Dict[str, Any]:
    missions = load_missions()
    mission["updated_at"] = _now()
    for i, item in enumerate(missions):
        if item.get("mission_id") == mission.get("mission_id"):
            missions[i] = mission
            save_missions(missions)
            return mission
    missions.insert(0, mission)
    save_missions(missions)
    return mission

def get_mission(mission_id: str) -> Optional[Dict[str, Any]]:
    for mission in load_missions():
        if mission.get("mission_id") == mission_id:
            return mission
    return None

def list_missions(limit: int = 20) -> List[Dict[str, Any]]:
    return load_missions()[:limit]
