from fastapi import APIRouter
from pydantic import BaseModel
from approval_engine_v8 import list_pending_approvals, approve_step, reject_step, run_approved_steps

router = APIRouter(prefix="/approval/v8", tags=["approval-v8"])

class ApprovalRequest(BaseModel):
    mission_id: str
    step_id: str

class RejectRequest(BaseModel):
    mission_id: str
    step_id: str
    reason: str = ""

@router.get("/health")
def health():
    return {"ok": True, "module": "approval-v8", "version": "v8.0.0-alpha4"}

@router.get("/pending")
def pending():
    return list_pending_approvals()

@router.post("/approve")
def approve(body: ApprovalRequest):
    return approve_step(body.mission_id, body.step_id)

@router.post("/reject")
def reject(body: RejectRequest):
    return reject_step(body.mission_id, body.step_id, body.reason)

@router.post("/{mission_id}/run-approved")
def run_approved(mission_id: str):
    return run_approved_steps(mission_id)
