import subprocess
from typing import Dict, Any
from llm.ollama import ask_ollama

SAFE_COMMANDS = {
    "system_info": ["bash", "-lc", "hostnamectl; echo; uptime; echo; free -h; echo; df -h"],
    "open_ports": ["bash", "-lc", "ss -tulpn"],
    "users": ["bash", "-lc", "cat /etc/passwd | cut -d: -f1,3,7"],
    "ssh_audit": ["bash", "-lc", "grep -Ei '^[# ]*(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|Port)' /etc/ssh/sshd_config || true"],
    "services": ["bash", "-lc", "systemctl --type=service --state=running --no-pager"],
    "updates": ["bash", "-lc", "apt list --upgradable 2>/dev/null || true"],
    "docker_ps": ["bash", "-lc", "docker ps 2>/dev/null || echo 'Docker not available'"],
}

def run_safe_command(name: str) -> Dict[str, Any]:
    if name not in SAFE_COMMANDS:
        return {"ok": False, "error": "Command not allowed"}

    result = subprocess.run(
        SAFE_COMMANDS[name],
        capture_output=True,
        text=True,
        timeout=40
    )

    return {
        "ok": result.returncode == 0,
        "command": name,
        "stdout": result.stdout[-10000:],
        "stderr": result.stderr[-5000:]
    }

def collect_security_audit():
    return {name: run_safe_command(name) for name in SAFE_COMMANDS.keys()}

def _count_updates(output: str) -> int:
    return len([x for x in output.splitlines() if "[upgradable from:" in x])

def parse_findings(audit):
    ports = audit.get("open_ports", {}).get("stdout", "")
    ssh = audit.get("ssh_audit", {}).get("stdout", "")
    updates = audit.get("updates", {}).get("stdout", "")
    system_info = audit.get("system_info", {}).get("stdout", "")
    docker = audit.get("docker_ps", {}).get("stdout", "")

    findings = []
    update_count = _count_updates(updates)

    if update_count > 0:
        findings.append({
            "id": "updates_available",
            "severity": "high" if update_count >= 20 else "medium",
            "title": f"{update_count} pachete au update disponibil",
            "requires_approval": True
        })

    if "0.0.0.0:8088" in ports or "*:8088" in ports:
        findings.append({
            "id": "hermes_api_public",
            "severity": "medium",
            "title": "Hermes API ascultă public pe 8088",
            "requires_approval": True
        })

    if "#PasswordAuthentication yes" in ssh or "PasswordAuthentication yes" in ssh:
        findings.append({
            "id": "ssh_password_possible",
            "severity": "high",
            "title": "SSH password authentication pare permisă/neclară",
            "requires_approval": True
        })

    if "#PermitRootLogin prohibit-password" in ssh or "PermitRootLogin yes" in ssh:
        findings.append({
            "id": "ssh_root_policy_unclear",
            "severity": "medium",
            "title": "Politica SSH pentru root este neclară",
            "requires_approval": True
        })

    if "Docker not available" in docker:
        findings.append({
            "id": "docker_not_available",
            "severity": "info",
            "title": "Docker nu este disponibil în acest container",
            "requires_approval": False
        })

    score = 100
    for f in findings:
        if f["severity"] == "high":
            score -= 18
        elif f["severity"] == "medium":
            score -= 10

    return {
        "environment": "lxc" if "Virtualization: lxc" in system_info else "unknown",
        "security_score": max(score, 0),
        "update_count": update_count,
        "findings": findings
    }

def security_plan(goal: str = "Securizează serverul"):
    audit = collect_security_audit()
    parsed = parse_findings(audit)

    prompt = f"""
Ești Hermes, agent local pentru homelab. Răspunde în română.

Goal:
{goal}

Context real:
{parsed}

Fă un plan scurt:
1. Rezumat
2. Probleme găsite
3. Acțiuni safe
4. Acțiuni care cer aprobare
5. Comenzi recomandate
"""

    analysis = ask_ollama(prompt)

    return {
        "ok": True,
        "goal": goal,
        "parsed": parsed,
        "audit": audit,
        "analysis": analysis
    }
