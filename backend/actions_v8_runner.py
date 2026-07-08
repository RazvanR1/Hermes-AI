from datetime import datetime, timezone
from typing import Dict, Any
import time

import actions_v8_linux  # noqa: F401 - registers Linux actions
import actions_v8_proxmox  # noqa: F401 - registers Proxmox actions
from actions_v8_registry import get_action, list_actions


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_registered_action(action_name: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}
    action = get_action(action_name)

    if not action:
        return {
            "ok": False,
            "action": action_name,
            "error": "Action not registered",
            "available_actions": list(list_actions().keys()),
        }

    started = _now()
    t0 = time.time()

    try:
        result = action.handler(params)
        duration = round(time.time() - t0, 3)
        return {
            "ok": bool(result.get("ok", False)),
            "action": action_name,
            "risk": action.risk,
            "dry_run": action.dry_run,
            "description": action.description,
            "started_at": started,
            "finished_at": _now(),
            "duration_seconds": duration,
            "result": result,
        }
    except Exception as e:
        duration = round(time.time() - t0, 3)
        return {
            "ok": False,
            "action": action_name,
            "risk": action.risk,
            "dry_run": action.dry_run,
            "description": action.description,
            "started_at": started,
            "finished_at": _now(),
            "duration_seconds": duration,
            "error": str(e),
        }
