from __future__ import annotations

import re
import unicodedata

from .models import Action, Intent, TargetType


ACTION_PATTERNS: list[tuple[Action, tuple[str, ...]]] = [
    (Action.RESTART, ("restart", "reboot", "reporneste", "repornire")),
    (Action.START, ("start", "porneste", "pornire")),
    (Action.STOP, ("stop", "opreste", "oprire", "shutdown")),
    (Action.STATUS, ("status", "stare", "verifica", "check")),
    (Action.ANALYZE, ("analizeaza", "analiza", "diagnostic", "de ce")),
    (Action.UPDATE, ("update", "actualizeaza", "upgrade")),
    (Action.BACKUP, ("backup", "salvare", "copie de siguranta")),
]


TARGET_PATTERNS: list[tuple[TargetType, tuple[str, ...], str]] = [
    (TargetType.HOME_ASSISTANT, ("home assistant", "homeassistant", "haos"), "homeassistant"),
    (TargetType.TRUENAS, ("truenas", "true nas"), "truenas"),
    (TargetType.OPNSENSE, ("opnsense", "opn sense"), "opnsense"),
    (TargetType.DOCKER, ("docker", "portainer"), "docker"),
    (TargetType.PROXMOX, ("proxmox", "pve"), "proxmox"),
]


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    without_diacritics = "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )
    return " ".join(without_diacritics.lower().strip().split())


class IntentEngine:
    def parse(self, text: str) -> Intent:
        raw_text = text.strip()
        normalized = normalize_text(raw_text)

        action = self._detect_action(normalized)
        target_type, target_id, target_name, skill = self._detect_target(normalized)

        confidence = self._calculate_confidence(
            action=action,
            target_type=target_type,
            target_id=target_id,
        )

        requires_confirmation = action in {
            Action.START,
            Action.STOP,
            Action.RESTART,
            Action.UPDATE,
            Action.BACKUP,
        }

        return Intent(
            raw_text=raw_text,
            action=action,
            target_type=target_type,
            target_id=target_id,
            target_name=target_name,
            skill=skill,
            confidence=confidence,
            requires_confirmation=requires_confirmation,
            metadata={"normalized_text": normalized},
        )

    @staticmethod
    def _detect_action(text: str) -> Action:
        for action, patterns in ACTION_PATTERNS:
            if any(pattern in text for pattern in patterns):
                return action
        return Action.UNKNOWN

    @staticmethod
    def _detect_target(
        text: str,
    ) -> tuple[TargetType, str | None, str | None, str]:
        vm_match = re.search(r"\bvm[\s_-]*(\d+)\b", text)
        if vm_match:
            target_id = vm_match.group(1)
            return TargetType.VM, target_id, f"VM{target_id}", "proxmox"

        lxc_match = re.search(r"\b(?:lxc|ct)[\s_-]*(\d+)\b", text)
        if lxc_match:
            target_id = lxc_match.group(1)
            return TargetType.LXC, target_id, f"LXC{target_id}", "proxmox"

        for target_type, patterns, skill in TARGET_PATTERNS:
            if any(pattern in text for pattern in patterns):
                return target_type, None, target_type.value, skill

        return TargetType.GENERIC, None, None, "generic"

    @staticmethod
    def _calculate_confidence(
        *,
        action: Action,
        target_type: TargetType,
        target_id: str | None,
    ) -> float:
        score = 0.2

        if action is not Action.UNKNOWN:
            score += 0.4

        if target_type is not TargetType.GENERIC:
            score += 0.25

        if target_id:
            score += 0.15

        return round(min(score, 1.0), 2)


intent_engine = IntentEngine()
