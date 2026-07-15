from __future__ import annotations

from .models import Intent


class SkillRouter:
    SUPPORTED_SKILLS = {
        "proxmox",
        "docker",
        "truenas",
        "homeassistant",
        "opnsense",
        "generic",
    }

    def resolve(self, intent: Intent) -> str:
        if intent.skill in self.SUPPORTED_SKILLS:
            return intent.skill
        return "generic"


skill_router = SkillRouter()
