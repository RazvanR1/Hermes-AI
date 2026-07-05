from fastapi import APIRouter
from api.response import ok

router = APIRouter()

@router.get("/agents")
def list_agents():
    return ok({
        "mode": "agents_v1",
        "agents": [
            {
                "name": "Guardian",
                "role": "Infrastructure monitor",
                "status": "running",
                "task": "Scanning infrastructure",
                "progress": 98,
                "objects": 127,
                "cpu": 8,
                "memory": 182,
                "last_action": "2 sec ago",
                "tone": "success"
            },
            {
                "name": "Planner",
                "role": "Execution planner",
                "status": "ready",
                "task": "Waiting for mission",
                "progress": 100,
                "objects": 6,
                "cpu": 3,
                "memory": 94,
                "last_action": "12 sec ago",
                "tone": "primary"
            },
            {
                "name": "Reasoner",
                "role": "Risk analysis",
                "status": "analyzing",
                "task": "Evaluating system health",
                "progress": 84,
                "objects": 42,
                "cpu": 6,
                "memory": 126,
                "last_action": "5 sec ago",
                "tone": "purple"
            },
            {
                "name": "Research",
                "role": "Docs and CVE research",
                "status": "idle",
                "task": "Standing by",
                "progress": 34,
                "objects": 3,
                "cpu": 1,
                "memory": 64,
                "last_action": "1 min ago",
                "tone": "warning"
            },
            {
                "name": "Executor",
                "role": "Controlled execution",
                "status": "waiting",
                "task": "Waiting for approval",
                "progress": 0,
                "objects": 0,
                "cpu": 0,
                "memory": 32,
                "last_action": "idle",
                "tone": "muted"
            }
        ]
    }, mode="agents_v1")
