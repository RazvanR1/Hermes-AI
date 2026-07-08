import subprocess
from typing import Dict, Any
from actions_v8_registry import Action, register
from skills.security import collect_security_audit, parse_findings


PRIVRUNNER = "/usr/bin/sudo /usr/local/sbin/hermes-privrunner"


def _run(cmd: str, timeout: int = 60) -> Dict[str, Any]:
    result = subprocess.run(
        ["bash", "-lc", cmd],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout[-12000:],
        "stderr": result.stderr[-8000:],
        "command": cmd,
    }


def linux_status(params: dict) -> Dict[str, Any]:
    return _run("hostnamectl; echo; uptime; echo; free -h; echo; df -h", timeout=30)


def linux_disk(params: dict) -> Dict[str, Any]:
    return _run("df -h", timeout=30)


def linux_memory(params: dict) -> Dict[str, Any]:
    return _run("free -h", timeout=30)


def linux_apt_update(params: dict) -> Dict[str, Any]:
    return _run(f"{PRIVRUNNER} linux.apt_update", timeout=240)


def linux_apt_upgrade_preview(params: dict) -> Dict[str, Any]:
    return _run("apt list --upgradable 2>/dev/null || true", timeout=60)


def security_audit(params: dict) -> Dict[str, Any]:
    audit = collect_security_audit()
    parsed = parse_findings(audit)
    return {
        "ok": True,
        "parsed": parsed,
        "audit": audit,
    }


def register_linux_actions() -> None:
    register(Action("linux.status", "SAFE", "Collect basic Linux system status", linux_status))
    register(Action("linux.disk", "SAFE", "Show disk usage", linux_disk))
    register(Action("linux.memory", "SAFE", "Show memory usage", linux_memory))
    register(Action("linux.apt_update", "SAFE", "Run apt update through Hermes privileged runner", linux_apt_update))
    register(Action("linux.apt_upgrade_preview", "SAFE", "Preview available package upgrades without installing", linux_apt_upgrade_preview, dry_run=True))
    register(Action("security.audit", "SAFE", "Run Hermes local security audit", security_audit))


register_linux_actions()
