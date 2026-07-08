from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime, timezone
import uuid


@dataclass
class NotificationEvent:
    type: str
    message: str
    level: str = "info"
    mission_id: Optional[str] = None
    step_id: Optional[str] = None
    source: str = "hermes"
    data: Dict[str, Any] = field(default_factory=dict)
    time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "NotificationEvent":
        return cls(
            type=raw.get("type", "EVENT"),
            message=raw.get("message", ""),
            level=raw.get("level", "info"),
            mission_id=raw.get("mission_id"),
            step_id=raw.get("step_id"),
            source=raw.get("source", "hermes"),
            data=raw.get("data") or {},
            time=raw.get("time") or datetime.now(timezone.utc).isoformat(),
            event_id=raw.get("event_id") or str(uuid.uuid4()),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "time": self.time,
            "type": self.type,
            "level": self.level,
            "mission_id": self.mission_id,
            "step_id": self.step_id,
            "message": self.message,
            "data": self.data,
            "source": self.source,
        }
