from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

import actions_v8_linux  # noqa: F401 - ensure Linux registration
import actions_v8_proxmox  # noqa: F401 - ensure Proxmox registration
from actions_v8_registry import list_actions, get_action
from actions_v8_runner import run_registered_action

router = APIRouter(prefix="/execution/v8", tags=["execution-v8"])


class RunActionRequest(BaseModel):
    action: str
    params: Dict[str, Any] = {}


@router.get("/health")
def health():
    return {
        "ok": True,
        "module": "execution-v8",
        "version": "v8.0.0-alpha5.2-proxmox"
    }


@router.get("/actions")
def actions():
    return {
        "ok": True,
        "actions": list_actions()
    }


@router.post("/run")
def run_action(body: RunActionRequest):
    action = get_action(body.action)
    if not action:
        return {
            "ok": False,
            "error": "Action not registered",
            "action": body.action,
            "available_actions": list(list_actions().keys())
        }

    if action.risk not in ("SAFE",):
        return {
            "ok": False,
            "error": "Only SAFE actions can be run directly in Alpha 5.2. Use Mission Approval for CONFIRM actions.",
            "action": body.action,
            "risk": action.risk,
        }

    return run_registered_action(body.action, body.params)
