from typing import Dict, Any
from datetime import datetime, timezone

from mission_store_v8 import get_mission, update_mission
from beta1_execution_pipeline_v8 import execute_approved_steps

try:
    from mission_events_v8 import mission_approved, mission_rejected
except Exception:
    mission_approved = mission_rejected = None


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

    mission["status"] = "approved"
    update_mission(mission)

    if mission_approved:
        mission_approved(mission_id, step_id, data={
            "action": found.get("action"),
            "params": found.get("params") or {},
        })

    execution_result = execute_approved_steps(mission_id)

    return {
        "ok": execution_result.get("ok", False),
        "approved_step": found,
        "execution": execution_result,
        "mission": execution_result.get("mission"),
    }


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

    if mission_rejected:
        mission_rejected(mission_id, step_id, reason=reason)

    return {"ok": True, "mission": mission, "rejected_step": found}


def run_approved_steps(mission_id: str) -> Dict[str, Any]:
    return execute_approved_steps(mission_id)
