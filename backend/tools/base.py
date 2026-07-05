from abc import ABC, abstractmethod
from typing import Any, Dict

class Tool(ABC):
    name: str = "tool"

    @abstractmethod
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        ...
