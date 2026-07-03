from fastapi import APIRouter
from pydantic import BaseModel
from api.response import ok
from brain import copilot

router = APIRouter()

class CopilotChatRequest(BaseModel):
    message: str

@router.post("/copilot/chat")
def copilot_chat(req: CopilotChatRequest):
    return ok(copilot.chat(req.message), mode="copilot_chat_v1")
