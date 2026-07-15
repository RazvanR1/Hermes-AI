from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class GuestType(StrEnum):
    VM = "vm"
    LXC = "lxc"


@dataclass(slots=True)
class ProxmoxGuestContext:
    vmid: int
    guest_type: GuestType

    exists: bool = False
    node: str | None = None
    name: str | None = None
    status: str = "unknown"
    running: bool = False
    locked: bool = False
    lock_reason: str | None = None
    backup_running: bool = False
    snapshot_count: int = 0

    cpu_usage: float | None = None
    memory_used_bytes: int | None = None
    memory_total_bytes: int | None = None
    memory_usage_percent: float | None = None
    uptime_seconds: int | None = None

    tags: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    raw_status: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
