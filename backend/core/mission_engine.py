from datetime import datetime, timezone
from typing import Dict, Any, List
from brain import context_engine
from core import planner
from core import reasoning

def run(mission: str, session_id: str = "dashboard") -> Dict[str, Any]:
    started = datetime.now(timezone.utc)

    ctx = context_engine.build(session_id)
    reason = reasoning.explain(ctx)
    plan = planner.build(mission, ctx)

    risk = "LOW"
    if reason.get("score", 100) < 80:
        risk = "MEDIUM"
    if reason.get("score", 100) < 70:
        risk = "HIGH"

    steps: List[Dict[str, Any]] = [
        {
            "agent": "Guardian",
            "status": "success",
            "message": "Infrastructure context collected.",
            "confidence": 0.96,
        },
        {
            "agent": "Planner",
            "status": "success",
            "message": "Execution plan created.",
            "confidence": 0.94,
            "output": plan,
        },
        {
            "agent": "Reasoner",
            "status": "success",
            "message": "Risk analysis completed.",
            "confidence": 0.92,
            "output": reason,
        },
        {
            "agent": "Executor",
            "status": "waiting_approval",
            "message": "Mission requires approval before execution.",
            "confidence": 0.9,
        },
    ]

    finished = datetime.now(timezone.utc)

    return {
        "mode": "mission_v1",
        "mission": mission,
        "session_id": session_id,
        "status": "waiting_approval",
        "risk": risk,
        "approval_required": True,
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
        "duration_ms": int((finished - started).total_seconds() * 1000),
        "reasoning": reason,
        "plan": plan,
        "steps": steps,
        "report": {
            "summary": f"Mission prepared: {mission}",
            "recommendation": "Review the plan and approve only during a safe maintenance window.",
        },
    }
