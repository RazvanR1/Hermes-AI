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

    def _approval_reply_markup(self, event: NotificationEvent) -> Dict[str, Any] | None:
        if event.type != "MISSION_APPROVAL_REQUIRED":
            return None

        waiting_steps = event.data.get("waiting_steps") or []
        if not waiting_steps:
            return None

        step_id = waiting_steps[0].get("id")
        if not event.mission_id or not step_id:
            return None

        return {
            "inline_keyboard": [
                [
                    {
                        "text": "✅ Approve",
                        "callback_data": f"approve:{event.mission_id}:{step_id}",
                    },
                    {
                        "text": "❌ Reject",
                        "callback_data": f"reject:{event.mission_id}:{step_id}",
                    },
                ]
            ]
        }

    def send(self, event: NotificationEvent) -> Dict[str, Any]:
        if not self.enabled():
            return {"ok": True, "skipped": True, "connector": self.name, "reason": "not_configured"}

        if send_telegram_message is None:
            return {"ok": False, "connector": self.name, "error": "telegram_v8 unavailable"}

        result = send_telegram_message(
            self.format(event),
            reply_markup=self._approval_reply_markup(event),
        )
        return {"ok": bool(result.get("ok")), "connector": self.name, "result": result}
