from fastapi import APIRouter
from pydantic import BaseModel
from api.response import ok
from planner_v2.planner import build_goal

router = APIRouter()

class Goal(BaseModel):
    goal: str

@router.post("/planner/v2")
def planner(req: Goal):
    return ok(
        build_goal(req.goal),
        mode="planner_v2"
    )
