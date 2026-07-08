from typing import Dict, Any, List
from datetime import datetime, timezone
import uuid

RISK_SAFE = "SAFE"
RISK_CONFIRM = "CONFIRM"
RISK_BLOCK = "BLOCK"

ACTION_POLICIES = {
    "security.audit": RISK_SAFE,
    "security.plan": RISK_SAFE,
    "security.apply_updates": RISK_CONFIRM,
    "security.fix_ssh": RISK_CONFIRM,
    "security.restart_ssh": RISK_CONFIRM,

    "linux.status": RISK_SAFE,
    "linux.disk": RISK_SAFE,
    "linux.memory": RISK_SAFE,

    "docker.inspect": RISK_SAFE,
    "docker.logs": RISK_SAFE,
    "docker.update": RISK_CONFIRM,
    "docker.restart": RISK_CONFIRM,

    "proxmox.nodes": RISK_SAFE,
    "proxmox.vm.status": RISK_SAFE,
    "proxmox.vm.reboot": RISK_CONFIRM,
    "proxmox.vm.reset": RISK_CONFIRM,
    "proxmox.vm.destroy": RISK_BLOCK,
}


def classify_action(action: str) -> str:
    return ACTION_POLICIES.get(action, RISK_CONFIRM)


def build_step(step_id: str, title: str, action: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    risk = classify_action(action)
    return {
        "id": step_id,
        "title": title,
        "action": action,
        "params": params or {},
        "risk": risk,
        "status": "planned",
        "requires_confirmation": risk == RISK_CONFIRM,
        "blocked": risk == RISK_BLOCK,
    }


def evaluate_plan(steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    safe = [s for s in steps if s.get("risk") == RISK_SAFE]
    confirm = [s for s in steps if s.get("risk") == RISK_CONFIRM]
    blocked = [s for s in steps if s.get("risk") == RISK_BLOCK]

    if blocked:
        overall = RISK_BLOCK
    elif confirm:
        overall = RISK_CONFIRM
    else:
        overall = RISK_SAFE

    return {
        "overall_risk": overall,
        "safe_count": len(safe),
        "confirm_count": len(confirm),
        "blocked_count": len(blocked),
        "safe": safe,
        "requires_confirmation": confirm,
        "blocked": blocked,
    }


def create_mission(goal: str, intent: Dict[str, Any], steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    evaluation = evaluate_plan(steps)
    return {
        "ok": True,
        "mission_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "goal": goal,
        "intent": intent,
        "status": "planned",
        "evaluation": evaluation,
        "steps": steps,
        "execution": {
            "mode": "preview",
            "message": "Alpha 2 creează misiuni și clasifică riscul. Execuția reală vine în Alpha 3."
        }
    }
