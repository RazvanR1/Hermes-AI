from fastapi import APIRouter
from pydantic import BaseModel

from operator_v8 import operator_chat

router = APIRouter(prefix="/operator/v8", tags=["operator-v8"])


class ChatRequest(BaseModel):
    message: str
    source: str = "api"
    user: str = "local"


@router.get("/health")
def health():
    return {
        "ok": True,
        "module": "operator-v8",
        "version": "v8.0.0-alpha5.3-operator-chat"
    }


@router.post("/chat")
def chat(body: ChatRequest):
    return operator_chat(body.message, source=body.source, user=body.user)
