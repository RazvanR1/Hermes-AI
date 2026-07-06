from typing import Dict, Any, List

from tools.dispatcher import execute as tool_execute
from missionlog.log import push


def execute_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []

    for step in plan.get("steps", []):
        title = step.get("title")
        tool = step.get("tool")
        action = step.get("action")
        params = step.get("params", {})

        if not tool or not action:
            raw_action = step.get("action", "")
            if "." in raw_action:
                tool, action = raw_action.split(".", 1)

        push("Executor", f"Running: {title}", "running")

        if not tool or not action:
            result = {
                "step": step.get("step"),
                "title": title,
                "ok": False,
                "error": "Missing tool or action.",
            }
            results.append(result)
            push("Executor", f"Failed: {title}", "error")
            break

        result = tool_execute(tool, action, **params)

        results.append({
            "step": step.get("step"),
            "title": title,
            "tool": tool,
            "action": action,
            "params": params,
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
