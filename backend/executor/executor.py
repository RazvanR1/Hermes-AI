from typing import Dict, Any, List

from tools.dispatcher import execute as tool_execute
from missionlog.log import push


def execute_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []

    for step in plan.get("steps", []):
        title = step.get("title")
        action = step.get("action", "")

        push("Executor", f"Running: {title}", "running")

        if "." not in action:
            result = {
                "step": step.get("step"),
                "title": title,
                "ok": False,
                "error": "Invalid action format.",
            }

            results.append(result)
            push("Executor", f"Failed: {title}", "error")
            break

        tool, tool_action = action.split(".", 1)
        result = tool_execute(tool, tool_action)

        results.append({
            "step": step.get("step"),
            "title": title,
            "tool": tool,
            "action": tool_action,
            "result": result,
        })

        if result.get("ok", False):
            push("Executor", f"Completed: {title}", "success")
        else:
            push("Executor", f"Failed: {title}", "error")
            break

    success = all(
        r.get("result", r).get("ok", False)
        for r in results
    )

    return {
        "ok": success,
        "steps": results,
    }
