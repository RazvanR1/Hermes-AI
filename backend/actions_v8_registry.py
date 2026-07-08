from dataclasses import dataclass
from typing import Callable, Dict, Any, Optional


@dataclass
class Action:
    name: str
    risk: str
    description: str
    handler: Callable[[dict], dict]
    dry_run: bool = False


_registry: Dict[str, Action] = {}


def register(action: Action) -> None:
    _registry[action.name] = action


def get_action(name: str) -> Optional[Action]:
    return _registry.get(name)


def list_actions() -> Dict[str, Any]:
    return {
        name: {
            "risk": action.risk,
            "description": action.description,
            "dry_run": action.dry_run,
        }
        for name, action in sorted(_registry.items())
    }
