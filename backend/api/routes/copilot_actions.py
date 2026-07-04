from fastapi import APIRouter
from pydantic import BaseModel

from api.response import ok
from brain import context
from core import impact

router = APIRouter()

class CopilotActionRequest(BaseModel):
    action: str
    payload: dict = {}

@router.post("/copilot/action")
def run_action(req: CopilotActionRequest):
    ctx = context.build()

    if req.action == "impact.opnsense":
        return ok(
            {
                "action": req.action,
                "title": "OPNsense impact",
                "result": impact.analyze("opnsense", ctx),
            },
            mode="copilot_action_v1",
        )

    return ok(
        {
            "action": req.action,
            "title": "Unknown action",
            "result": {
                "message": "Action not implemented yet."
            },
        },
        mode="copilot_action_v1",
    )
