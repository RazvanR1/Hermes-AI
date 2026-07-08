from fastapi import APIRouter
from pydantic import BaseModel

from brain_v8 import detect_intent
from skill_registry_v8 import build_skill_plan, registry_status
from executor_v8 import create_mission
from mission_store_v8 import save_mission, list_missions, get_mission
from execution_v8 import run_safe_steps

router = APIRouter(prefix="/mission/v8", tags=["mission-v8"])

class MissionGoal(BaseModel):
    goal: str

@router.get("/health")
def health():
    return {
        "ok": True,
        "module": "mission-v8",
        "version": "v8-alpha-safe-executor"
    }

@router.get("/registry")
def registry():
    return registry_status()

@router.post("/plan")
def plan(body: MissionGoal):
    intent = detect_intent(body.goal)
    steps = build_skill_plan(body.goal, intent)
    return create_mission(body.goal, intent, steps)

@router.post("/create")
def create(body: MissionGoal):
    intent = detect_intent(body.goal)
    steps = build_skill_plan(body.goal, intent)
    mission = create_mission(body.goal, intent, steps)
    mission["status"] = "planned"
    return save_mission(mission)

@router.get("/list")
def list_all(limit: int = 20):
    return {
        "ok": True,
        "missions": list_missions(limit=limit)
    }

@router.get("/{mission_id}")
def read(mission_id: str):
    mission = get_mission(mission_id)
    if not mission:
        return {
            "ok": False,
            "error": "Mission not found",
            "mission_id": mission_id
        }
    return {
        "ok": True,
        "mission": mission
    }

@router.post("/{mission_id}/run-safe")
def run_safe(mission_id: str):
    return run_safe_steps(mission_id)
