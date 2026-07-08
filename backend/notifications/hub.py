from typing import Dict, Any, List

from notifications.models import NotificationEvent
from notifications.registry import get_connectors


def notify(event: Dict[str, Any] | NotificationEvent) -> Dict[str, Any]:
    notification_event = event if isinstance(event, NotificationEvent) else NotificationEvent.from_dict(event)

    results: List[Dict[str, Any]] = []
    for connector in get_connectors():
        try:
            results.append(connector.send(notification_event))
        except Exception as exc:
            results.append({
                "ok": False,
                "connector": getattr(connector, "name", connector.__class__.__name__),
                "error": str(exc),
            })

    return {
        "ok": all(r.get("ok") for r in results),
        "event": notification_event.to_dict(),
        "results": results,
    }
