from __future__ import annotations

from .models import (
    Action,
    ExecutionPlan,
    Intent,
    PlanStep,
    RiskLevel,
)


class Planner:
    def build(self, intent: Intent) -> ExecutionPlan:
        if intent.action is Action.UNKNOWN:
            return ExecutionPlan(
                goal=intent.raw_text,
                intent=intent,
                steps=[],
                estimated_duration_seconds=0,
                rollback_available=False,
            )

        target = intent.target_name or intent.target_type.value

        if intent.action is Action.STATUS:
            steps = [
                PlanStep(
                    id="query-status",
                    title=f"Verifică statusul {target}",
                    action="status",
                    skill=intent.skill,
                    risk=RiskLevel.SAFE,
                    requires_confirmation=False,
                    params=self._target_params(intent),
                )
            ]
            duration = 3
            rollback = False

        elif intent.action is Action.RESTART:
            steps = [
                PlanStep(
                    id="validate-target",
                    title=f"Validează ținta {target}",
                    action="validate",
                    skill=intent.skill,
                    risk=RiskLevel.SAFE,
                    requires_confirmation=False,
                    params=self._target_params(intent),
                ),
                PlanStep(
                    id="restart-target",
                    title=f"Repornește {target}",
                    action="restart",
                    skill=intent.skill,
                    risk=RiskLevel.MEDIUM,
                    requires_confirmation=True,
                    params=self._target_params(intent),
                ),
                PlanStep(
                    id="verify-target",
                    title=f"Verifică revenirea {target}",
                    action="status",
                    skill=intent.skill,
                    risk=RiskLevel.SAFE,
                    requires_confirmation=False,
                    params=self._target_params(intent),
                ),
            ]
            duration = 30
            rollback = False

        elif intent.action in {Action.START, Action.STOP}:
            steps = [
                PlanStep(
                    id=f"{intent.action.value}-target",
                    title=f"{intent.action.value.capitalize()} {target}",
                    action=intent.action.value,
                    skill=intent.skill,
                    risk=RiskLevel.MEDIUM,
                    requires_confirmation=True,
                    params=self._target_params(intent),
                ),
                PlanStep(
                    id="verify-target",
                    title=f"Verifică statusul {target}",
                    action="status",
                    skill=intent.skill,
                    risk=RiskLevel.SAFE,
                    requires_confirmation=False,
                    params=self._target_params(intent),
                ),
            ]
            duration = 20
            rollback = intent.action is Action.STOP

        else:
            steps = [
                PlanStep(
                    id=f"{intent.action.value}-target",
                    title=f"{intent.action.value.capitalize()} {target}",
                    action=intent.action.value,
                    skill=intent.skill,
                    risk=RiskLevel.LOW,
                    requires_confirmation=intent.requires_confirmation,
                    params=self._target_params(intent),
                )
            ]
            duration = 15
            rollback = False

        return ExecutionPlan(
            goal=intent.raw_text,
            intent=intent,
            steps=steps,
            estimated_duration_seconds=duration,
            rollback_available=rollback,
        )

    @staticmethod
    def _target_params(intent: Intent) -> dict[str, str]:
        params: dict[str, str] = {
            "target_type": intent.target_type.value,
        }

        if intent.target_id:
            params["target_id"] = intent.target_id

        if intent.target_name:
            params["target_name"] = intent.target_name

        return params


planner = Planner()
