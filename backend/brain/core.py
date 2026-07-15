from __future__ import annotations

from .guardian import guardian
from .intent_engine import intent_engine
from .models import MissionContext
from .planner import planner
from .responder import responder
from .skill_router import skill_router


class HermesBrain:
    def analyze(self, text: str) -> MissionContext:
        intent = intent_engine.parse(text)
        intent.skill = skill_router.resolve(intent)

        plan = planner.build(intent)
        decision = guardian.evaluate(plan)

        reasoning = [
            f"Intent detectat: {intent.action.value}",
            f"Țintă detectată: {intent.target_name or intent.target_type.value}",
            f"Skill selectat: {intent.skill}",
            *decision.reasons,
        ]

        return MissionContext(
            goal=text.strip(),
            intent=intent,
            plan=plan,
            guardian=decision,
            environment=intent.skill,
            reasoning=reasoning,
        )

    def explain(self, text: str) -> str:
        context = self.analyze(text)
        return responder.compose(context)


brain = HermesBrain()
