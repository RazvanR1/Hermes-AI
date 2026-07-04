from fastapi import APIRouter
from pydantic import BaseModel

from api.response import ok
from brain import context_engine
from core import planner

router = APIRouter()

class PlannerRequest(BaseModel):
    task:str

@router.post("/planner")
def build_plan(req:PlannerRequest):

    ctx=context_engine.build("dashboard")

    return ok(
        planner.build(req.task,ctx),
        mode="plan_v1"
    )
