from typing import Dict, Any
from skills.security import collect_security_audit, parse_findings, security_plan

def run_action(action: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    params = params or {}

    if action == "security.audit":
        audit = collect_security_audit()
        parsed = parse_findings(audit)
        return {"ok": True, "action": action, "result": {"parsed": parsed, "audit": audit}}

    if action == "security.plan":
        goal = params.get("goal", "Securizează serverul")
        plan = security_plan(goal)
        return {"ok": True, "action": action, "result": plan}

    if action == "security.apply_updates":
        return {
            "ok": True,
            "action": action,
            "dry_run": True,
            "result": {
                "message": "Alpha 4 dry-run: ar rula apt update și ar pregăti upgrade-ul, dar nu modifică sistemul.",
                "commands_preview": [
                    "apt update",
                    "apt list --upgradable",
                    "apt upgrade"
                ],
                "requires_real_execution_in": "Alpha 5"
            }
        }

    if action == "security.fix_ssh":
        return {
            "ok": True,
            "action": action,
            "dry_run": True,
            "result": {
                "message": "Alpha 4 dry-run: ar face backup la sshd_config și ar propune PasswordAuthentication no / PermitRootLogin no, dar nu aplică schimbarea.",
                "commands_preview": [
                    "cp /etc/ssh/sshd_config /etc/ssh/sshd_config.hermes.bak",
                    "sshd -t",
                    "systemctl reload ssh"
                ],
                "requires_real_execution_in": "Alpha 5"
            }
        }

    if action == "linux.status":
        import subprocess
        r = subprocess.run(["bash", "-lc", "hostnamectl; uptime; free -h; df -h"], capture_output=True, text=True, timeout=30)
        return {"ok": r.returncode == 0, "action": action, "result": {"stdout": r.stdout[-10000:], "stderr": r.stderr[-5000:]}}

    return {"ok": False, "action": action, "error": "Action runner not implemented for this action"}
