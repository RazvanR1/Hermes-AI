from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from api.response import ok
from executor.executor import execute_plan
from history.history import add as add_history

router = APIRouter()


class ApprovalRequest(BaseModel):
    mission: str
    approved: bool
    plan: Dict[str, Any]


@router.post("/missions/approve")
def approve(req: ApprovalRequest):
    if not req.approved:
        return ok({
            "status": "cancelled",
            "message": "Mission cancelled.",
            "mission": req.mission,
        })

    executed = execute_plan(req.plan)

    history_item = add_history(
        req.mission,
        "completed" if executed.get("ok") else "failed",
        executed,
    )

    return ok({
        "history": history_item,
        "status": "completed" if executed.get("ok") else "failed",
        "mission": req.mission,
        "executed": executed,
        "events": [
            {"agent": "Executor", "status": "starting"},
            {"agent": "Executor", "status": "executing"},
            {"agent": "Guardian", "status": "verifying"},
            {
                "agent": "Executor",
                "status": "completed" if executed.get("ok") else "failed",
            },
        ],
    })
