from __future__ import annotations

import re
from typing import Any, Dict, List

from brain import Action, MissionContext, TargetType, brain
from brain_v8 import detect_intent
from executor_v8 import build_step, create_mission
from mission_events_v8 import (
    mission_approval_required,
    mission_created,
)
from mission_store_v8 import save_mission


def _extract_target_legacy(message: str) -> Dict[str, Any]:
    """
    Compatibility fallback for request formats not yet covered by Hermes Brain.
    This function will be removed after Brain intent coverage is complete.
    """
    normalized = message.lower()

    vm_match = re.search(
        r"\b(vm|qemu)\s*#?\s*(\d+)\b",
        normalized,
    )
    lxc_match = re.search(
        r"\b(lxc|ct|container)\s*#?\s*(\d+)\b",
        normalized,
    )

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


def _has_any(message: str, words: list[str]) -> bool:
    return any(word in message for word in words)


def _detect_force_action(
    message: str,
    target: Dict[str, Any],
) -> str | None:
    """
    Preserve force-reset and force-stop commands that are not represented
    in the first Brain Action model yet.
    """
    normalized = message.lower()
    target_type = target.get("type")

    if not target_type:
        return None

    prefix = (
        "proxmox.vm"
        if target_type == "vm"
        else "proxmox.lxc"
    )

    if (
        target_type == "vm"
        and _has_any(
            normalized,
            [
                "reset",
                "force reset",
                "restart forțat",
                "restart fortat",
            ],
        )
    ):
        return "proxmox.vm.reset"

    if _has_any(
        normalized,
        [
            "force stop",
            "oprește forțat",
            "opreste fortat",
        ],
    ):
        return f"{prefix}.stop"

    return None


def _brain_target(
    context: MissionContext,
) -> Dict[str, Any]:
    intent = context.intent

    if intent.target_type not in {
        TargetType.VM,
        TargetType.LXC,
    }:
        return {}

    if not intent.target_id:
        return {}

    return {
        "type": intent.target_type.value,
        "vmid": int(intent.target_id),
        "node": "proxmox",
    }


def _brain_proxmox_action(
    context: MissionContext,
    target: Dict[str, Any],
) -> str | None:
    if not target:
        return None

    target_type = target["type"]
    prefix = (
        "proxmox.vm"
        if target_type == "vm"
        else "proxmox.lxc"
    )

    action_map = {
        Action.STATUS: f"{prefix}.status",
        Action.START: f"{prefix}.start",
        Action.STOP: f"{prefix}.shutdown",
        Action.RESTART: f"{prefix}.reboot",
    }

    return action_map.get(context.intent.action)


def _build_operator_steps(
    message: str,
    legacy_intent: Dict[str, Any],
    brain_context: MissionContext,
) -> List[Dict[str, Any]]:
    del legacy_intent  # retained in signature for compatibility and clarity

    target = _brain_target(brain_context)

    if not target:
        target = _extract_target_legacy(message)

    action = _detect_force_action(message, target)

    if not action:
        action = _brain_proxmox_action(
            brain_context,
            target,
        )

    if action:
        target_label = target.get(
            "type",
            "",
        ).upper()
        vmid = target.get("vmid")

        return [
            build_step(
                step_id="operator-proxmox-action",
                title=(
                    f"{action} pentru "
                    f"{target_label} {vmid}"
                ),
                action=action,
                params={
                    "node": target.get(
                        "node",
                        "proxmox",
                    ),
                    "vmid": vmid,
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


def _prepare_status_for_approval(
    mission: Dict[str, Any],
) -> Dict[str, Any]:
    waiting = 0

    for step in mission.get("steps", []):
        requires_confirmation = bool(
            step.get("requires_confirmation")
        )
        risk_requires_confirmation = (
            step.get("risk") == "CONFIRM"
        )

        if (
            requires_confirmation
            or risk_requires_confirmation
        ):
            step["status"] = (
                "waiting_confirmation"
            )
            waiting += 1

    mission["status"] = (
        "waiting_confirmation"
        if waiting
        else "planned"
    )

    return mission


def _brain_mission_summary(
    context: MissionContext,
) -> Dict[str, Any]:
    intent = context.intent
    guardian = context.guardian
    plan = context.plan

    return {
        "intent": intent.action.value,
        "target_type": intent.target_type.value,
        "target_id": intent.target_id,
        "target_name": intent.target_name,
        "skill": intent.skill,
        "confidence": intent.confidence,
        "risk": guardian.risk.value,
        "allowed": guardian.allowed,
        "requires_approval": (
            guardian.requires_approval
        ),
        "estimated_duration_seconds": (
            plan.estimated_duration_seconds
        ),
        "rollback_available": (
            plan.rollback_available
        ),
        "reasoning": context.reasoning,
    }


def operator_chat(
    message: str,
    source: str = "api",
    user: str = "local",
) -> Dict[str, Any]:
    clean_message = message.strip()

    if not clean_message:
        return {
            "ok": False,
            "error": "Mesajul nu poate fi gol.",
            "message": message,
            "source": source,
            "user": user,
        }

    # New Hermes Brain analysis.
    brain_context = brain.analyze(clean_message)

    # Existing v8 intent remains active during the incremental migration,
    # because create_mission() currently expects its existing schema.
    legacy_intent = detect_intent(clean_message)

    steps = _build_operator_steps(
        clean_message,
        legacy_intent,
        brain_context,
    )

    mission = create_mission(
        clean_message,
        legacy_intent,
        steps,
    )

    mission["source"] = source
    mission["requested_by"] = user
    mission["brain"] = _brain_mission_summary(
        brain_context
    )

    mission = _prepare_status_for_approval(
        mission
    )
    mission = save_mission(mission)

    mission_created(mission)

    requires_approval = [
        step
        for step in mission.get("steps", [])
        if (
            step.get("requires_confirmation")
            or step.get("risk") == "CONFIRM"
        )
    ]

    if requires_approval:
        mission_approval_required(mission)

    safe_steps = [
        step
        for step in mission.get("steps", [])
        if step.get("risk") == "SAFE"
    ]

    return {
        "ok": True,
        "message": clean_message,
        "source": source,
        "user": user,

        # Compatibility field used by the current frontend and mission engine.
        "intent": legacy_intent,

        # New structured Brain response.
        "brain": brain_context.to_dict(),
        "assistant_message": brain.explain(
            clean_message
        ),

        "mission": mission,
        "summary": {
            "mission_id": mission.get(
                "mission_id"
            ),
            "status": mission.get("status"),
            "overall_risk": mission.get(
                "evaluation",
                {},
            ).get("overall_risk"),
            "safe_steps": len(safe_steps),
            "requires_approval": len(
                requires_approval
            ),
            "brain_risk": (
                brain_context.guardian.risk.value
            ),
            "brain_allowed": (
                brain_context.guardian.allowed
            ),
            "brain_confidence": (
                brain_context.intent.confidence
            ),
            "estimated_duration_seconds": (
                brain_context.plan
                .estimated_duration_seconds
            ),
        },
    }
