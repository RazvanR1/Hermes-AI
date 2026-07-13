from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any

from telegram_v8 import (
    send_telegram_message,
    telegram_configured,
    format_mission_event,
    answer_callback_query,
)
from approval_engine_v8 import approve_step, reject_step
from beta1_execution_pipeline_v8 import execute_approved_steps

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
        "version": "v0.9-telegram-interactive",
        "configured": telegram_configured(),
    }


@router.post("/send-test")
def send_test(body: SendTestRequest):
    return send_telegram_message(body.text, chat_id=body.chat_id)


@router.post("/send-event")
def send_event(body: SendEventRequest):
    text = format_mission_event(body.event)
    return send_telegram_message(text, chat_id=body.chat_id)


@router.post("/webhook")
def webhook(update: Dict[str, Any]):
    callback = update.get("callback_query")

    if not callback:
        return {"ok": True, "ignored": True, "reason": "not_callback_query"}

    callback_id = callback.get("id")
    data = callback.get("data") or ""
    message = callback.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = str(chat.get("id")) if chat.get("id") is not None else None

    parts = data.split("|")
    if len(parts) != 3:
        if callback_id:
            answer_callback_query(callback_id, "Invalid Hermes callback")
        return {"ok": False, "error": "invalid_callback_data", "data": data}

    command, mission_id, step_id = parts

    if command in ("approve", "a"):
        approval = approve_step(mission_id, step_id)
        if callback_id:
            answer_callback_query(callback_id, "Approved. Running mission...")
        send_telegram_message(
            f"✅ <b>Hermes</b>\nApproved mission <code>{mission_id}</code>\n▶️ Running...",
            chat_id=chat_id,
        )
        execution = execute_approved_steps(mission_id)
        return {"ok": True, "command": command, "approval": approval, "execution": execution}

    if command in ("reject", "r"):
        rejection = reject_step(mission_id, step_id, "Rejected from Telegram")
        if callback_id:
            answer_callback_query(callback_id, "Rejected.")
        send_telegram_message(
            f"❌ <b>Hermes</b>\nRejected mission <code>{mission_id}</code>",
            chat_id=chat_id,
        )
        return {"ok": True, "command": command, "rejection": rejection}

    if callback_id:
        answer_callback_query(callback_id, "Unknown Hermes command")
    return {"ok": False, "error": "unknown_command", "command": command}
