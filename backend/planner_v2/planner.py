import re
from inventory.inventory import inventory


def build_goal(goal: str):
    inv = inventory.collect()

    if not inv.get("ok"):
        return {
            "ok": False,
            "error": "Inventory unavailable"
        }

    summary = inv["inventory"]["summary"]
    goal_lower = goal.lower()
    plan = []

    vm_match = re.search(r"(vm|ct|lxc)\s*#?\s*(\d+)", goal_lower)
    vmid = int(vm_match.group(2)) if vm_match else None

    if vmid and any(x in goal_lower for x in ["restart", "reboot", "repornește", "reporneste"]):
        plan = [
            {
                "step": 1,
                "title": f"Reboot VM {vmid}",
                "tool": "proxmox_action",
                "action": "reboot",
                "params": {
                    "node": "proxmox",
                    "vmid": vmid
                }
            }
        ]

    elif vmid and any(x in goal_lower for x in ["shutdown", "oprește", "opreste"]):
        plan = [
            {
                "step": 1,
                "title": f"Shutdown VM {vmid}",
                "tool": "proxmox_action",
                "action": "shutdown",
                "params": {
                    "node": "proxmox",
                    "vmid": vmid
                }
            }
        ]

    elif vmid and "start" in goal_lower:
        plan = [
            {
                "step": 1,
                "title": f"Start VM {vmid}",
                "tool": "proxmox_action",
                "action": "start",
                "params": {
                    "node": "proxmox",
                    "vmid": vmid
                }
            }
        ]

    elif "update proxmox" in goal_lower or "actualizează proxmox" in goal_lower:
        plan = [
            {
                "step": 1,
                "title": "Verify infrastructure health",
                "tool": "shell",
                "action": "hostname",
                "params": {}
            },
            {
                "step": 2,
                "title": "Verify available memory",
                "tool": "shell",
                "action": "memory",
                "params": {}
            },
            {
                "step": 3,
                "title": "Verify storage",
                "tool": "shell",
                "action": "disk",
                "params": {}
            },
            {
                "step": 4,
                "title": "Check Proxmox node",
                "tool": "proxmox",
                "action": "nodes",
                "params": {}
            }
        ]

    else:
        plan = [
            {
                "step": 1,
                "title": "Check infrastructure",
                "tool": "proxmox",
                "action": "nodes",
                "params": {}
            }
        ]

    return {
        "ok": True,
        "version": "1.0",
        "goal": goal,
        "inventory": summary,
        "estimated_duration": max(len(plan) * 2, 1),
        "risk": "LOW",
        "steps": plan
    }
