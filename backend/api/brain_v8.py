from fastapi import APIRouter
from pydantic import BaseModel
from brain_v8 import build_brain_plan

router = APIRouter(prefix="/brain/v8", tags=["brain-v8"])


class BrainGoal(BaseModel):
    goal: str


@router.get("/health")
def health():
    return {
        "ok": True,
        "module": "brain-v8",
        "version": "v8.0.0-alpha1"
    }


@router.post("/goal")
def goal(body: BrainGoal):
    return build_brain_plan(body.goal)
