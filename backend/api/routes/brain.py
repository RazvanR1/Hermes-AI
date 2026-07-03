from fastapi import APIRouter
from pydantic import BaseModel
from providers.operations import sysadmin
from api.response import ok

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    return ok(sysadmin.run(req.message), mode="brain_chat_v1")
