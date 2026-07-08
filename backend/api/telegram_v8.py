from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any

from telegram_v8 import send_telegram_message, telegram_configured, format_mission_event

router = APIRouter(prefix="/telegram/v8", tags=["telegram-v8"])


class SendTestRequest(BaseModel):
    text: str = "Hermes Telegram test ✅"
    chat_id: Optional[str] = None


class SendEventRequest(BaseModel):
    event: Dict[str, Any]
    chat_id: Optional[str] = None


@router.get("/health")
def health():
    return {
        "ok": True,
        "module": "telegram-v8",
        "version": "v0.9-telegram-foundation",
        "configured": telegram_configured(),
    }


@router.post("/send-test")
def send_test(body: SendTestRequest):
    return send_telegram_message(body.text, chat_id=body.chat_id)


@router.post("/send-event")
def send_event(body: SendEventRequest):
    text = format_mission_event(body.event)
    return send_telegram_message(text, chat_id=body.chat_id)
