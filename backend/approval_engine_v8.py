from typing import Dict, Any
from datetime import datetime, timezone
from mission_store_v8 import get_mission, update_mission
from action_runner_v8 import run_action

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def list_pending_approvals() -> Dict[str, Any]:
    from mission_store_v8 import load_missions
    pending = []

    for mission in load_missions():
        for step in mission.get("steps", []):
            if step.get("status") == "waiting_confirmation":
                pending.append({
                    "mission_id": mission.get("mission_id"),
                    "goal": mission.get("goal"),
                    "step_id": step.get("id"),
                    "title": step.get("title"),
                    "action": step.get("action"),
                    "risk": step.get("risk"),
                })

    return {
        "ok": True,
        "pending": pending,
        "count": len(pending)
    }

def approve_step(mission_id: str, step_id: str) -> Dict[str, Any]:
    mission = get_mission(mission_id)
    if not mission:
        return {"ok": False, "error": "Mission not found", "mission_id": mission_id}

    found = None
    for step in mission.get("steps", []):
        if step.get("id") == step_id:
            found = step
            break

    if not found:
        return {"ok": False, "error": "Step not found", "mission_id": mission_id, "step_id": step_id}

    if found.get("risk") == "BLOCK" or found.get("blocked"):
        return {"ok": False, "error": "Blocked step cannot be approved", "step": found}

    found["approved"] = True
    found["approved_at"] = _now()
    found["status"] = "approved"

    mission.setdefault("logs", []).append({
        "time": _now(),
        "level": "approval",
        "message": f"Approved step {step_id}"
    })

    mission["status"] = "approved_pending_execution"
    update_mission(mission)
    return {"ok": True, "mission": mission, "approved_step": found}

def reject_step(mission_id: str, step_id: str, reason: str = "") -> Dict[str, Any]:
    mission = get_mission(mission_id)
    if not mission:
        return {"ok": False, "error": "Mission not found", "mission_id": mission_id}

    found = None
    for step in mission.get("steps", []):
        if step.get("id") == step_id:
            found = step
            break

    if not found:
        return {"ok": False, "error": "Step not found", "mission_id": mission_id, "step_id": step_id}

    found["approved"] = False
    found["rejected"] = True
    found["rejected_at"] = _now()
    found["reject_reason"] = reason
    found["status"] = "rejected"

    mission.setdefault("logs", []).append({
        "time": _now(),
        "level": "approval",
        "message": f"Rejected step {step_id}: {reason}"
    })

    if all(s.get("status") in ("done", "rejected", "blocked") for s in mission.get("steps", [])):
        mission["status"] = "completed_with_rejections"
    else:
        mission["status"] = "waiting_confirmation"

    update_mission(mission)
    return {"ok": True, "mission": mission, "rejected_step": found}

def run_approved_steps(mission_id: str) -> Dict[str, Any]:
    mission = get_mission(mission_id)
    if not mission:
        return {"ok": False, "error": "Mission not found", "mission_id": mission_id}

    mission["status"] = "running_approved"
    mission.setdefault("logs", []).append({
        "time": _now(),
        "level": "info",
        "message": "Starting approved-step execution"
    })

    executed = []
    skipped = []
    failed = []

    for step in mission.get("steps", []):
        if not step.get("approved"):
            skipped.append(step)
            continue

        if step.get("status") == "done":
            skipped.append(step)
            continue

        action = step.get("action")
        step["status"] = "running"
        step["started_at"] = _now()

        result = run_action(action, step.get("params") or {})
        step["result"] = result
        step["finished_at"] = _now()

        if result.get("ok"):
            step["status"] = "done"
            executed.append(step)
        else:
            step["status"] = "failed"
            failed.append(step)

    waiting = [s for s in mission.get("steps", []) if s.get("status") == "waiting_confirmation"]

    if failed:
        mission["status"] = "failed"
    elif waiting:
        mission["status"] = "waiting_confirmation"
    else:
        mission["status"] = "completed"

    mission["execution"] = {
        "mode": "approved-only",
        "executed_count": len(executed),
        "skipped_count": len(skipped),
        "failed_count": len(failed),
        "waiting_confirmation_count": len(waiting),
    }

    mission["logs"].append({
        "time": _now(),
        "level": "info",
        "message": f"Approved execution finished with status {mission['status']}"
    })

    update_mission(mission)
    return {"ok": True, "mission": mission}
