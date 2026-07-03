from fastapi import APIRouter
from pydantic import BaseModel

from api.response import ok
from brain import copilot

router = APIRouter()

class CopilotChatRequest(BaseModel):
    session_id: str = "default"
    message: str

@router.post("/copilot/chat")
def chat(req: CopilotChatRequest):
    result = copilot.chat(
        req.message,
        session_id=req.session_id,
    )
    return ok(result, mode="copilot_chat_v1")
