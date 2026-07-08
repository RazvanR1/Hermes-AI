import os
from typing import Dict, Any, Optional
import requests


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def telegram_configured() -> bool:
    return bool(_env("TELEGRAM_BOT_TOKEN") and _env("TELEGRAM_CHAT_ID"))


def send_telegram_message(
    text: str,
    chat_id: Optional[str] = None,
    parse_mode: str = "HTML",
    disable_web_page_preview: bool = True,
) -> Dict[str, Any]:
    token = _env("TELEGRAM_BOT_TOKEN")
    target_chat_id = chat_id or _env("TELEGRAM_CHAT_ID")

    if not token:
        return {"ok": False, "error": "Missing TELEGRAM_BOT_TOKEN"}

    if not target_chat_id:
        return {"ok": False, "error": "Missing TELEGRAM_CHAT_ID"}

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": target_chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": disable_web_page_preview,
    }

    try:
        r = requests.post(url, json=payload, timeout=15)
        data = r.json()
        return {
            "ok": r.ok and data.get("ok") is True,
            "http_status": r.status_code,
            "telegram": data,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_mission_event(event: Dict[str, Any]) -> str:
    event_type = event.get("type", "EVENT")
    mission_id = event.get("mission_id") or "-"
    step_id = event.get("step_id") or "-"
    message = event.get("message") or ""
    level = event.get("level") or "info"

    icon = {
        "MISSION_APPROVED": "✅",
        "MISSION_RUNNING": "▶️",
        "MISSION_COMPLETED": "🏁",
        "MISSION_FAILED": "❌",
        "STEP_STARTED": "🔧",
        "STEP_FINISHED": "✅",
        "STEP_FAILED": "❌",
    }.get(event_type, "ℹ️")

    return (
        f"{icon} <b>Hermes</b>\n"
        f"<b>Event:</b> {event_type}\n"
        f"<b>Level:</b> {level}\n"
        f"<b>Mission:</b> <code>{mission_id}</code>\n"
        f"<b>Step:</b> <code>{step_id}</code>\n"
        f"<b>Message:</b> {message}"
    )
