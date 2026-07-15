from __future__ import annotations

from .models import MissionContext


class Responder:
    def compose(self, context: MissionContext) -> str:
        intent = context.intent
        guardian = context.guardian
        plan = context.plan

        target = (
            intent.target_name
            or intent.target_id
            or intent.target_type.value
        )

        approval_text = (
            "Este necesară aprobarea ta înainte de execuție."
            if guardian.requires_approval
            else "Nu este necesară aprobarea pentru această operație."
        )

        return (
            f"Am înțeles cererea: „{context.goal}”. "
            f"Ținta identificată este {target}, iar skill-ul selectat este "
            f"{intent.skill}. Planul conține {len(plan.steps)} pas/pasi, "
            f"cu risc {guardian.risk.value}. {approval_text}"
        )


responder = Responder()
