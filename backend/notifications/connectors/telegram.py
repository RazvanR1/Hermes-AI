from typing import Dict, Any
from notifications.models import NotificationEvent

try:
    from telegram_v8 import send_telegram_message
except Exception:
    send_telegram_message = None


class TelegramNotificationConnector:
    name = "telegram"

    def enabled(self) -> bool:
        import os
        return bool(os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"))

    def format(self, event: NotificationEvent) -> str:
        icon = {
            "MISSION_CREATED": "🧠",
            "MISSION_APPROVAL_REQUIRED": "⚠️",
            "MISSION_APPROVED": "✅",
            "MISSION_RUNNING": "▶️",
            "MISSION_COMPLETED": "🏁",
            "MISSION_FAILED": "❌",
            "STEP_STARTED": "🔧",
            "STEP_FINISHED": "✅",
        }.get(event.type, "ℹ️")

        return (
            f"{icon} <b>Hermes</b>\n"
            f"<b>Event:</b> {event.type}\n"
            f"<b>Level:</b> {event.level}\n"
            f"<b>Mission:</b> <code>{event.mission_id or '-'}</code>\n"
            f"<b>Step:</b> <code>{event.step_id or '-'}</code>\n"
            f"<b>Message:</b> {event.message}"
        )

    def send(self, event: NotificationEvent) -> Dict[str, Any]:
        if not self.enabled():
            return {"ok": True, "skipped": True, "connector": self.name, "reason": "not_configured"}

        if send_telegram_message is None:
            return {"ok": False, "connector": self.name, "error": "telegram_v8 unavailable"}

        result = send_telegram_message(self.format(event))
        return {"ok": bool(result.get("ok")), "connector": self.name, "result": result}
