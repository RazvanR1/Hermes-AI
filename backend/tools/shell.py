import subprocess
from typing import Dict, Any
from .base import Tool

SAFE_COMMANDS = {
    "hostname": ["hostname"],
    "uptime": ["uptime"],
    "disk": ["df", "-h"],
    "memory": ["free", "-h"],
    "kernel": ["uname", "-r"],
}

class ShellTool(Tool):
    name = "shell"

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        if action not in SAFE_COMMANDS:
            return {
                "ok": False,
                "error": f"Action '{action}' not allowed."
            }

        result = subprocess.run(
            SAFE_COMMANDS[action],
            capture_output=True,
            text=True
        )

        return {
            "ok": result.returncode == 0,
            "action": action,
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
        }

shell = ShellTool()
