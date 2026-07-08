from typing import Dict, Any
from tools.shell import shell
from tools.docker import docker_tool
from tools.proxmox import proxmox_tool
from tools.proxmox_actions import proxmox_actions

TOOLS = {
    "shell": shell,
    "docker": docker_tool,
    "proxmox": proxmox_tool,
    "proxmox_action": proxmox_actions,
}

def execute(tool: str, action: str, **kwargs) -> Dict[str, Any]:
    if tool not in TOOLS:
        return {
            "ok": False,
            "error": f"Unknown tool '{tool}'"
        }

    return TOOLS[tool].execute(action, **kwargs)
