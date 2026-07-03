from core import taskplanner

def execute(task: str, ctx=None):
    ctx = ctx or {}

    plan = taskplanner.build(task)

    report = {
        "mode": "task_runtime_v1",
        "task": task,
        "status": "completed",
        "steps": [],
    }

    for step in plan["steps"]:

        result = {
            "step": step["step"],
            "action": step["action"],
            "description": step["description"],
            "status": "ok",
        }

        # Decision step
        if step["action"] == "decision.proxmox.update":
            from core import decision

            d = decision.decide("proxmox.update", ctx)

            result["decision"] = d

            if not d["allowed"]:
                result["status"] = "blocked"

                report["status"] = "blocked"

                report["steps"].append(result)

                break

        report["steps"].append(result)

    return report
