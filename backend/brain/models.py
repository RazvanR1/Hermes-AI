from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class Action(StrEnum):
    STATUS = "status"
    START = "start"
    STOP = "stop"
    RESTART = "restart"
    ANALYZE = "analyze"
    UPDATE = "update"
    BACKUP = "backup"
    UNKNOWN = "unknown"


class TargetType(StrEnum):
    VM = "vm"
    LXC = "lxc"
    CONTAINER = "container"
    PROXMOX = "proxmox"
    DOCKER = "docker"
    TRUENAS = "truenas"
    HOME_ASSISTANT = "homeassistant"
    OPNSENSE = "opnsense"
    GENERIC = "generic"


class RiskLevel(StrEnum):
    SAFE = "SAFE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BLOCKED = "BLOCKED"


@dataclass(slots=True)
class Intent:
    raw_text: str
    action: Action
    target_type: TargetType
    target_id: str | None = None
    target_name: str | None = None
    skill: str = "generic"
    confidence: float = 0.0
    requires_confirmation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PlanStep:
    id: str
    title: str
    action: str
    skill: str
    risk: RiskLevel
    requires_confirmation: bool
    params: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ExecutionPlan:
    goal: str
    intent: Intent
    steps: list[PlanStep]
    estimated_duration_seconds: int
    rollback_available: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class GuardianDecision:
    risk: RiskLevel
    requires_approval: bool
    allowed: bool
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class MissionContext:
    goal: str
    intent: Intent
    plan: ExecutionPlan
    guardian: GuardianDecision
    environment: str
    reasoning: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
