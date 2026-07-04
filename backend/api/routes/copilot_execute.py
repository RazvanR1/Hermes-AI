from fastapi import APIRouter
from pydantic import BaseModel

from api.response import ok

from brain import context_engine
from brain import copilot

from core import reasoning
from core import planner

router = APIRouter()

class ExecuteRequest(BaseModel):
    session_id: str = "dashboard"
    message: str


@router.post("/copilot/execute")
def execute(req: ExecuteRequest):

    ctx = context_engine.build(req.session_id)

    reasoning_result = reasoning.explain(ctx)

    planner_result = planner.build(
        req.message,
        ctx
    )

    copilot_result = copilot.chat(
        req.message,
        req.session_id
    )

    return ok(
        {
            "mode": "execute_v1",

            "answer": copilot_result["answer"],

            "intent": copilot_result["intent"],

            "reasoning": reasoning_result,

            "plan": planner_result,

            "actions": copilot_result["actions"],

            "history": copilot_result["history"]

        },
        mode="execute_v1"
    )
