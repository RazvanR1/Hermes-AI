from __future__ import annotations

from .models import (
    ExecutionPlan,
    GuardianDecision,
    RiskLevel,
)


RISK_ORDER = {
    RiskLevel.SAFE: 0,
    RiskLevel.LOW: 1,
    RiskLevel.MEDIUM: 2,
    RiskLevel.HIGH: 3,
    RiskLevel.BLOCKED: 4,
}


class Guardian:
    def evaluate(self, plan: ExecutionPlan) -> GuardianDecision:
        if not plan.steps:
            return GuardianDecision(
                risk=RiskLevel.BLOCKED,
                requires_approval=False,
                allowed=False,
                reasons=["Nu a putut fi construit un plan de execuție."],
            )

        highest_risk = max(
            (step.risk for step in plan.steps),
            key=lambda risk: RISK_ORDER[risk],
        )

        requires_approval = any(
            step.requires_confirmation for step in plan.steps
        )

        reasons = [
            f"Planul conține {len(plan.steps)} pas/pasi.",
            f"Riscul maxim detectat este {highest_risk.value}.",
        ]

        if requires_approval:
            reasons.append("Cel puțin un pas necesită aprobarea utilizatorului.")
        else:
            reasons.append("Planul nu modifică infrastructura sau are risc sigur.")

        allowed = highest_risk is not RiskLevel.BLOCKED

        return GuardianDecision(
            risk=highest_risk,
            requires_approval=requires_approval,
            allowed=allowed,
            reasons=reasons,
        )


guardian = Guardian()
