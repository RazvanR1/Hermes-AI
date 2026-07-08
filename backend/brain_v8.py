from typing import Dict, Any
from llm.ollama import ask_ollama


def detect_intent(goal: str) -> Dict[str, Any]:
    g = goal.lower()

    if any(x in g for x in ["securizează", "securizeaza", "security", "ssh", "firewall", "fail2ban"]):
        return {
            "intent": "security.plan",
            "skill": "security",
            "risk": "CONFIRM",
            "reason": "Cererea este legată de securitate."
        }

    if any(x in g for x in ["vm", "lxc", "ct", "proxmox", "reset", "restart", "reboot", "shutdown", "pornește", "porneste", "oprește", "opreste"]):
        return {
            "intent": "proxmox.plan",
            "skill": "proxmox",
            "risk": "CONFIRM",
            "reason": "Cererea este legată de Proxmox/VM/LXC."
        }

    if any(x in g for x in ["docker", "container", "compose", "portainer", "image", "volum"]):
        return {
            "intent": "docker.plan",
            "skill": "docker",
            "risk": "CONFIRM",
            "reason": "Cererea este legată de Docker."
        }

    if any(x in g for x in ["truenas", "nas", "smb", "zfs", "pool", "hdd", "disc", "disk", "smart"]):
        return {
            "intent": "storage.plan",
            "skill": "storage",
            "risk": "CONFIRM",
            "reason": "Cererea este legată de storage/TrueNAS."
        }

    if any(x in g for x in ["home assistant", "haos", "automation", "automatizare", "clima", "gree"]):
        return {
            "intent": "homeassistant.plan",
            "skill": "homeassistant",
            "risk": "CONFIRM",
            "reason": "Cererea este legată de Home Assistant."
        }

    if any(x in g for x in ["lent", "greu", "performanta", "performanță", "lag", "load", "cpu", "ram", "swap"]):
        return {
            "intent": "performance.diagnose",
            "skill": "linux",
            "risk": "SAFE",
            "reason": "Cererea este legată de performanță."
        }

    return {
        "intent": "general.plan",
        "skill": "general",
        "risk": "SAFE",
        "reason": "Nu s-a detectat un skill specific."
    }


def build_brain_plan(goal: str) -> Dict[str, Any]:
    intent = detect_intent(goal)

    prompt = f"""
Ești Hermes v8 Brain, AI Operator pentru homelab.

Obiectiv:
{goal}

Intent detectat:
{intent}

Reguli:
- Răspunde în română.
- Nu executa comenzi.
- Nu inventa date despre server.
- Creează un plan scurt și practic.
- Nu recomanda comenzi distructive.
- Împarte în:
  1. Ce am înțeles
  2. Ce verific întâi
  3. Ce skill trebuie folosit
  4. Ce este SAFE
  5. Ce cere aprobare
"""

    analysis = ask_ollama(prompt)

    return {
        "ok": True,
        "version": "v8.0.0-alpha1",
        "goal": goal,
        "intent": intent,
        "analysis": analysis,
    }
