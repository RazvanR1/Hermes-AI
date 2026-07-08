from datetime import datetime, timezone
from typing import Dict, Any
from mission_store_v8 import get_mission, update_mission
from action_runner_v8 import run_action

def now():
    return datetime.now(timezone.utc).isoformat()

def run_safe_steps(mission_id: str) -> Dict[str, Any]:
    mission = get_mission(mission_id)
    if not mission:
        return {"ok": False, "error": "Mission not found", "mission_id": mission_id}

    mission["status"] = "running"
    mission.setdefault("logs", [])
    mission["logs"].append({"time": now(), "level": "info", "message": "Running SAFE steps"})

    executed = 0
    waiting = 0
    blocked = 0
    failed = 0

    for step in mission.get("steps", []):
        risk = step.get("risk")
        action = step.get("action")

        if step.get("status") == "done":
            continue

        if risk == "BLOCK" or step.get("blocked"):
            step["status"] = "blocked"
            blocked += 1
            continue

        if risk == "CONFIRM" or step.get("requires_confirmation"):
            step["status"] = "waiting_confirmation"
            waiting += 1
            continue

        if risk == "SAFE":
            step["status"] = "running"
            step["started_at"] = now()

            result = run_action(action, step.get("params") or {})

            step["result"] = result
            step["finished_at"] = now()

            if result.get("ok"):
                step["status"] = "done"
                executed += 1
            else:
                step["status"] = "failed"
                failed += 1

    if failed:
        mission["status"] = "failed"
    elif waiting:
        mission["status"] = "waiting_confirmation"
    elif blocked:
        mission["status"] = "blocked"
    else:
        mission["status"] = "completed"

    mission["execution"] = {
        "mode": "safe-only",
        "executed_count": executed,
        "waiting_confirmation_count": waiting,
        "blocked_count": blocked,
        "failed_count": failed,
    }

    mission["logs"].append({
        "time": now(),
        "level": "info",
        "message": f"SAFE execution finished: {mission['status']}"
    })

    update_mission(mission)
    return {"ok": True, "mission": mission}
