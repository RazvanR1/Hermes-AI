from typing import Dict, Any
from tools.shell import shell
from tools.docker import docker_tool

TOOLS = {
    "shell": shell,
    "docker": docker_tool,
}

def execute(tool: str, action: str, **kwargs) -> Dict[str, Any]:
    if tool not in TOOLS:
        return {
            "ok": False,
            "error": f"Unknown tool '{tool}'"
        }

    return TOOLS[tool].execute(action, **kwargs)
