from fastapi import APIRouter
from pydantic import BaseModel
from api.response import ok
from core import mission_engine

router = APIRouter()

class MissionRequest(BaseModel):
    session_id: str = "dashboard"
    mission: str

@router.post("/missions/run")
def run_mission(req: MissionRequest):
    return ok(
        mission_engine.run(req.mission, req.session_id),
        mode="mission_v1",
    )
