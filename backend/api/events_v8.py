from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from event_bus_v8 import load_events, events_for_mission, emit_event

router = APIRouter(prefix="/events/v8", tags=["events-v8"])


class EmitTestRequest(BaseModel):
    event_type: str = "TEST_EVENT"
    mission_id: str | None = None
    step_id: str | None = None
    message: str = "Test event"
    data: Dict[str, Any] = {}


@router.get("/health")
def health():
    return {
        "ok": True,
        "module": "events-v8",
        "version": "v8-events-core"
    }


@router.get("/list")
def list_all(limit: int = 100):
    return {
        "ok": True,
        "events": load_events(limit=limit),
    }


@router.get("/mission/{mission_id}")
def mission_events(mission_id: str, limit: int = 200):
    return {
        "ok": True,
        "mission_id": mission_id,
        "events": events_for_mission(mission_id, limit=limit),
    }


@router.post("/emit-test")
def emit_test(body: EmitTestRequest):
    event = emit_event(
        body.event_type,
        mission_id=body.mission_id,
        step_id=body.step_id,
        message=body.message,
        data=body.data,
        source="api-test",
    )
    return {
        "ok": True,
        "event": event,
    }
