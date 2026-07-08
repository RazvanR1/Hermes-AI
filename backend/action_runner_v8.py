from typing import Dict, Any, Optional

from actions_v8_runner import run_registered_action


def run_action(action: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return run_registered_action(action, params or {})
