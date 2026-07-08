from typing import Dict, Any
from datetime import datetime, timezone
from mission_store_v8 import get_mission, update_mission
from action_runner_v8 import run_action

RISK_SAFE = "SAFE"
RISK_CONFIRM = "CONFIRM"
RISK_BLOCK = "BLOCK"

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def run_safe_steps(mission_id: str) -> Dict[str, Any]:
    mission = get_mission(mission_id)
    if not mission:
        return {"ok": False, "error": "Mission not found", "mission_id": mission_id}

    mission["status"] = "running"
    mission.setdefault("logs", [])
    mission["logs"].append({"time": _now(), "level": "info", "message": "Starting SAFE-only execution"})

    executed, waiting_confirmation, blocked, failed = [], [], [], []

    for step in mission.get("steps", []):
        risk = step.get("risk")
        action = step.get("action")

        if risk == RISK_BLOCK or step.get("blocked"):
            step["status"] = "blocked"
            blocked.append(step)
            continue

        if risk == RISK_CONFIRM or step.get("requires_confirmation"):
            step["status"] = "waiting_confirmation"
            waiting_confirmation.append(step)
            continue

        if risk == RISK_SAFE:
            step["status"] = "running"
            step["started_at"] = _now()
            try:
                params = dict(step.get("params") or {})
                params.setdefault("goal", mission.get("goal"))
                result = run_action(action, params)
                step["result"] = result
                step["finished_at"] = _now()
                if result.get("ok"):
                    step["status"] = "done"
                    executed.append(step)
                else:
                    step["status"] = "failed"
                    failed.append(step)
            except Exception as e:
                step["status"] = "failed"
                step["error"] = str(e)
                step["finished_at"] = _now()
                failed.append(step)

    if failed:
        mission["status"] = "failed"
    elif waiting_confirmation:
        mission["status"] = "waiting_confirmation"
    elif blocked:
        mission["status"] = "blocked"
    else:
        mission["status"] = "completed"

    mission["execution"] = {
        "mode": "safe-only",
        "executed_count": len(executed),
        "waiting_confirmation_count": len(waiting_confirmation),
        "blocked_count": len(blocked),
        "failed_count": len(failed),
    }

    mission["logs"].append({"time": _now(), "level": "info", "message": f"SAFE execution finished with status {mission['status']}"})
    update_mission(mission)
    return {"ok": True, "mission": mission}
