from fastapi import APIRouter
from api.response import ok
from executor.executor import execute_plan

router = APIRouter()

demo_plan = {
    "steps": [
        {
            "step": 1,
            "title": "Hostname",
            "action": "shell.hostname",
        },
        {
            "step": 2,
            "title": "Memory",
            "action": "shell.memory",
        },
        {
            "step": 3,
            "title": "Kernel",
            "action": "shell.kernel",
        }
    ]
}

@router.post("/executor/demo")
def demo():
    return ok(execute_plan(demo_plan))
