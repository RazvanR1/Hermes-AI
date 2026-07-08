from typing import Dict, Any
from event_bus_v8 import emit_event


MISSION_CREATED = "MISSION_CREATED"
MISSION_APPROVED = "MISSION_APPROVED"
MISSION_REJECTED = "MISSION_REJECTED"
MISSION_RUNNING = "MISSION_RUNNING"
MISSION_COMPLETED = "MISSION_COMPLETED"
MISSION_FAILED = "MISSION_FAILED"
STEP_STARTED = "STEP_STARTED"
STEP_FINISHED = "STEP_FINISHED"
STEP_FAILED = "STEP_FAILED"


def mission_created(mission: Dict[str, Any]):
    return emit_event(
        MISSION_CREATED,
        mission_id=mission.get("mission_id"),
        message=f"Mission created: {mission.get('goal')}",
        data={
            "goal": mission.get("goal"),
            "status": mission.get("status"),
            "risk": mission.get("evaluation", {}).get("overall_risk"),
        },
        source="mission",
    )


def mission_approved(mission_id: str, step_id: str | None = None, data: Dict[str, Any] | None = None):
    return emit_event(
        MISSION_APPROVED,
        mission_id=mission_id,
        step_id=step_id,
        message=f"Mission/step approved: {step_id or mission_id}",
        data=data or {},
        source="approval",
    )


def mission_rejected(mission_id: str, step_id: str | None = None, reason: str = ""):
    return emit_event(
        MISSION_REJECTED,
        mission_id=mission_id,
        step_id=step_id,
        level="warning",
        message=f"Mission/step rejected: {step_id or mission_id}",
        data={"reason": reason},
        source="approval",
    )


def mission_running(mission_id: str):
    return emit_event(
        MISSION_RUNNING,
        mission_id=mission_id,
        message="Mission running",
        source="execution",
    )


def mission_completed(mission_id: str, data: Dict[str, Any] | None = None):
    return emit_event(
        MISSION_COMPLETED,
        mission_id=mission_id,
        message="Mission completed",
        data=data or {},
        source="execution",
    )


def mission_failed(mission_id: str, error: str = "", data: Dict[str, Any] | None = None):
    return emit_event(
        MISSION_FAILED,
        mission_id=mission_id,
        level="error",
        message=f"Mission failed: {error}",
        data=data or {},
        source="execution",
    )


def step_started(mission_id: str, step_id: str, action: str = ""):
    return emit_event(
        STEP_STARTED,
        mission_id=mission_id,
        step_id=step_id,
        message=f"Step started: {step_id}",
        data={"action": action},
        source="execution",
    )


def step_finished(mission_id: str, step_id: str, action: str = "", ok: bool = True, data: Dict[str, Any] | None = None):
    return emit_event(
        STEP_FINISHED if ok else STEP_FAILED,
        mission_id=mission_id,
        step_id=step_id,
        level="info" if ok else "error",
        message=f"Step {'finished' if ok else 'failed'}: {step_id}",
        data={"action": action, **(data or {})},
        source="execution",
    )
