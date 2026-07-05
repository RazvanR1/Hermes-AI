from fastapi import APIRouter
from pydantic import BaseModel
from api.response import ok

router = APIRouter()

class ApprovalRequest(BaseModel):
    mission: str
    approved: bool

@router.post("/missions/approve")
def approve(req: ApprovalRequest):

    if not req.approved:
        return ok({
            "status": "cancelled",
            "message": "Mission cancelled."
        })

    return ok({
        "status": "executing",
        "message": "Mission approved.",
        "events":[
            {"agent":"Executor","status":"starting"},
            {"agent":"Executor","status":"executing"},
            {"agent":"Guardian","status":"verifying"},
            {"agent":"Executor","status":"completed"}
        ]
    })
