from fastapi import APIRouter
from pydantic import BaseModel
from skills.security import collect_security_audit, parse_findings, security_plan

router = APIRouter(prefix="/security", tags=["security"])

class SecurityGoal(BaseModel):
    goal: str = "Securizează serverul"

@router.get("/health")
def health():
    return {"ok": True, "module": "security"}

@router.post("/audit")
def audit():
    raw = collect_security_audit()
    parsed = parse_findings(raw)
    return {"ok": True, "parsed": parsed, "audit": raw}

@router.post("/plan")
def plan(body: SecurityGoal):
    return security_plan(body.goal)
