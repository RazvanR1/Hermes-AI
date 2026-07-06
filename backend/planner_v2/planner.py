from inventory.inventory import inventory

def build_goal(goal: str):
    inv = inventory.collect()

    if not inv.get("ok"):
        return {
            "ok": False,
            "error": "Inventory unavailable"
        }

    summary = inv["inventory"]["summary"]

    plan = []

    goal_lower = goal.lower()

    if "update proxmox" in goal_lower or "actualizează proxmox" in goal_lower:
        plan = [
            {
                "step": 1,
                "title": "Verify infrastructure health",
                "action": "shell.hostname"
            },
            {
                "step": 2,
                "title": "Verify available memory",
                "action": "shell.memory"
            },
            {
                "step": 3,
                "title": "Verify storage",
                "action": "shell.disk"
            },
            {
                "step": 4,
                "title": "Check Proxmox node",
                "action": "proxmox.nodes"
            }
        ]

    elif "restart" in goal_lower:
        plan = [
            {
                "step": 1,
                "title": "Verify infrastructure",
                "action": "proxmox.nodes"
            }
        ]

    return {
        "ok": True,
        "goal": goal,
        "inventory": summary,
        "estimated_duration": len(plan) * 2,
        "risk": "LOW",
        "steps": plan
    }
