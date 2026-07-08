from typing import Dict, Any, List
from executor_v8 import build_step


def plan_security(goal: str, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        build_step("security-audit", "Rulează audit de securitate", "security.audit"),
        build_step("security-plan", "Generează plan de securizare", "security.plan"),
        build_step("security-updates", "Aplică update-uri de securitate", "security.apply_updates"),
        build_step("security-ssh", "Întărește configurația SSH", "security.fix_ssh"),
    ]


def plan_docker(goal: str, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        build_step("docker-inspect", "Inspectează containerele Docker", "docker.inspect"),
        build_step("docker-logs", "Verifică logurile containerelor relevante", "docker.logs"),
        build_step("docker-update", "Actualizează imaginile Docker", "docker.update"),
        build_step("docker-restart", "Recreează/repornește containerele afectate", "docker.restart"),
    ]


def plan_proxmox(goal: str, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        build_step("proxmox-nodes", "Verifică nodurile Proxmox", "proxmox.nodes"),
        build_step("proxmox-status", "Verifică statusul VM/LXC", "proxmox.vm.status"),
        build_step("proxmox-action", "Aplică acțiunea cerută asupra VM/LXC", "proxmox.vm.reboot"),
    ]


def plan_linux(goal: str, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        build_step("linux-status", "Verifică statusul sistemului", "linux.status"),
        build_step("linux-memory", "Verifică memoria și swap-ul", "linux.memory"),
        build_step("linux-disk", "Verifică spațiul pe disc", "linux.disk"),
    ]


def plan_general(goal: str, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        build_step("linux-status", "Verifică statusul general al sistemului", "linux.status"),
    ]


SKILL_PLANNERS = {
    "security": plan_security,
    "docker": plan_docker,
    "proxmox": plan_proxmox,
    "linux": plan_linux,
    "storage": plan_linux,
    "homeassistant": plan_general,
    "general": plan_general,
}


def build_skill_plan(goal: str, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
    skill = intent.get("skill", "general")
    planner = SKILL_PLANNERS.get(skill, plan_general)
    return planner(goal, intent)


def registry_status() -> Dict[str, Any]:
    return {
        "ok": True,
        "skills": sorted(SKILL_PLANNERS.keys()),
        "version": "v8.0.0-alpha2"
    }
