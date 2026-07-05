from typing import Dict, Any, List
from tools.dispatcher import execute as tool_execute

def execute_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []

    for step in plan.get("steps", []):

        action = step.get("action", "")

        if "." not in action:
            results.append({
                "step": step.get("step"),
                "title": step.get("title"),
                "ok": False,
                "error": "Invalid action format."
            })
            continue

        tool, tool_action = action.split(".", 1)

        result = tool_execute(tool, tool_action)

        results.append({
            "step": step.get("step"),
            "title": step.get("title"),
            "tool": tool,
            "action": tool_action,
            "result": result,
        })

        if not result.get("ok", False):
            break

    success = all(
        r.get("result", {}).get("ok", False)
        for r in results
    )

    return {
        "ok": success,
        "steps": results,
    }
