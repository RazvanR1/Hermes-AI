from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from api.response import ok
from tools.dispatcher import execute

router = APIRouter()

class DispatchRequest(BaseModel):
    tool: str
    action: str
    params: Dict[str, Any] = {}

@router.post("/tools/execute")
def execute_tool(req: DispatchRequest):
    return ok(
        execute(req.tool, req.action, **req.params),
        mode="tool_execution_v1"
    )
