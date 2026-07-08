from typing import List, Any

from notifications.connectors.telegram import TelegramNotificationConnector


def get_connectors() -> List[Any]:
    return [
        TelegramNotificationConnector(),
    ]
