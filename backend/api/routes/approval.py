from fastapi import APIRouter
from pydantic import BaseModel
from api.response import ok
from core import planner
from brain import context_engine
from executor.executor import execute_plan

router = APIRouter()

class ApprovalRequest(BaseModel):
    mission: str
    approved: bool
    session_id: str = "dashboard"

@router.post("/missions/approve")
def approve(req: ApprovalRequest):

    if not req.approved:
        return ok({
            "status": "cancelled",
            "message": "Mission cancelled."
        }, mode="approval_v1")

    ctx = context_engine.build(req.session_id)
    plan = planner.build(req.mission, ctx)

    # momentan executăm doar acțiunile safe shell.*
    safe_plan = {
        "steps": [
            {
                "step": 1,
                "title": "Hostname check",
                "action": "shell.hostname",
            },
            {
                "step": 2,
                "title": "Memory check",
                "action": "shell.memory",
            },
            {
                "step": 3,
                "title": "Disk check",
                "action": "shell.disk",
            },
            {
                "step": 4,
                "title": "Kernel check",
                "action": "shell.kernel",
            }
        ]
    }

    execution = execute_plan(safe_plan)

    return ok({
        "status": "completed" if execution.get("ok") else "failed",
        "message": "Mission approved and executed in safe mode.",
        "mission": req.mission,
        "planned": plan,
        "executed": execution,
        "events": [
            {"agent": "Executor", "status": "starting"},
            {"agent": "Executor", "status": "executing"},
            {"agent": "Guardian", "status": "verifying"},
            {"agent": "Executor", "status": "completed" if execution.get("ok") else "failed"},
        ]
    }, mode="approval_v1")
