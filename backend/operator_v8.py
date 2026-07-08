import re
from typing import Dict, Any, List

from brain_v8 import detect_intent
from executor_v8 import build_step, create_mission
from mission_store_v8 import save_mission


def _extract_target(message: str) -> Dict[str, Any]:
    m = message.lower()

    vm_match = re.search(r"\b(vm|qemu)\s*#?\s*(\d+)\b", m)
    lxc_match = re.search(r"\b(lxc|ct|container)\s*#?\s*(\d+)\b", m)

    if vm_match:
        return {
            "type": "vm",
            "vmid": int(vm_match.group(2)),
            "node": "proxmox",
        }

    if lxc_match:
        return {
            "type": "lxc",
            "vmid": int(lxc_match.group(2)),
            "node": "proxmox",
        }

    return {}


def _has_any(m: str, words: list[str]) -> bool:
    return any(w in m for w in words)


def _detect_proxmox_action(message: str, target: Dict[str, Any]) -> str | None:
    m = message.lower()
    t = target.get("type")

    if not t:
        return None

    prefix = "proxmox.vm" if t == "vm" else "proxmox.lxc"

    # IMPORTANT: order matters.
    # "repornește" contains "pornește", so reboot must be detected before start.

    if _has_any(m, ["status", "stare", "verifică", "verifica"]):
        return f"{prefix}.status"

    if t == "vm" and _has_any(m, ["reset", "force reset", "restart forțat", "restart fortat"]):
        return "proxmox.vm.reset"

    if _has_any(m, ["restart", "repornește", "reporneste", "reboot"]):
        return f"{prefix}.reboot"

    if _has_any(m, ["shutdown", "oprește", "opreste", "inchide", "închide"]):
        return f"{prefix}.shutdown"

    if _has_any(m, ["stop", "force stop", "oprește forțat", "opreste fortat"]):
        return f"{prefix}.stop"

    if _has_any(m, ["pornește", "porneste", "start"]):
        return f"{prefix}.start"

    return None


def _build_operator_steps(message: str, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
    target = _extract_target(message)
    action = _detect_proxmox_action(message, target)

    if action:
        title = f"{action} pentru {target.get('type', '').upper()} {target.get('vmid')}"
        return [
            build_step(
                step_id="operator-proxmox-action",
                title=title,
                action=action,
                params={
                    "node": target.get("node", "proxmox"),
                    "vmid": target.get("vmid"),
                },
            )
        ]

    return [
        build_step(
            step_id="operator-linux-status",
            title="Verifică statusul general Linux",
            action="linux.status",
            params={},
        )
    ]


def _prepare_status_for_approval(mission: Dict[str, Any]) -> Dict[str, Any]:
    waiting = 0

    for step in mission.get("steps", []):
        if step.get("risk") == "CONFIRM" or step.get("requires_confirmation"):
            step["status"] = "waiting_confirmation"
            waiting += 1

    if waiting:
        mission["status"] = "waiting_confirmation"
    else:
        mission["status"] = "planned"

    return mission


def operator_chat(message: str, source: str = "api", user: str = "local") -> Dict[str, Any]:
    intent = detect_intent(message)
    steps = _build_operator_steps(message, intent)

    mission = create_mission(message, intent, steps)
    mission["source"] = source
    mission["requested_by"] = user
    mission = _prepare_status_for_approval(mission)

    mission = save_mission(mission)

    requires_approval = [
        step for step in mission.get("steps", [])
        if step.get("requires_confirmation") or step.get("risk") == "CONFIRM"
    ]

    safe_steps = [
        step for step in mission.get("steps", [])
        if step.get("risk") == "SAFE"
    ]

    return {
        "ok": True,
        "message": message,
        "source": source,
        "user": user,
        "intent": intent,
        "mission": mission,
        "summary": {
            "mission_id": mission.get("mission_id"),
            "status": mission.get("status"),
            "overall_risk": mission.get("evaluation", {}).get("overall_risk"),
            "safe_steps": len(safe_steps),
            "requires_approval": len(requires_approval),
        }
    }
