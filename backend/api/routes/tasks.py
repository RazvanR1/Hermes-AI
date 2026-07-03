from fastapi import APIRouter
from pydantic import BaseModel
from brain import context
from core import taskqueue
from api.response import ok

router = APIRouter()

class TaskCreate(BaseModel):
    task: str

@router.get("/tasks")
def list_tasks():
    return ok(taskqueue.list_tasks(50), mode="tasks_list_v1")

@router.post("/tasks")
def create_task(req: TaskCreate):
    return ok(taskqueue.create(req.task), mode="task_create_v1")

@router.post("/tasks/{task_id}/run")
def run_task(task_id: int):
    ctx = context.build()
    return ok(taskqueue.run(task_id, ctx=ctx), mode="task_run_v1")
