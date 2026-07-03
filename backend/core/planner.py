def build_plan(context):
    inventory = context.get("inventory", {}) or {}
    health = context.get("health", {}) or {}

    plan = {
        "version": "v6-core-planner",
        "health": health.get("score") or health.get("health_score"),
        "critical": [],
        "warnings": [],
        "recommendations": [],
        "safe_actions": [],
        "confirm_actions": [],
        "dangerous_actions": [],
        "inventory_summary": inventory.get("summary", {}),
    }

    for warning in inventory.get("warnings", []):
        plan["warnings"].append(warning)

    summary = inventory.get("summary", {})
    if summary.get("docker_exited", 0):
        plan["warnings"].append(f"{summary['docker_exited']} containere Docker nu rulează")
        plan["safe_actions"].append({
            "action": "inspect_docker_exited",
            "label": "Verifică containerele Docker oprite",
            "policy": "SAFE",
        })

    if summary.get("opnsense") == "error":
        plan["warnings"].append("OPNsense nu a putut fi verificat prin API")

    return plan
