from fastapi import APIRouter
from pydantic import BaseModel
from api.response import ok
from tools.shell import shell

router = APIRouter()

class ToolRequest(BaseModel):
    action: str

@router.post("/tools/shell")
def run_tool(req: ToolRequest):
    return ok(shell.execute(req.action))
