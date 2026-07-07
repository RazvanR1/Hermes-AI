from typing import Dict, Any, List

from tools.dispatcher import execute as tool_execute
from missionlog.log import push
from agents.proxmox.tasks import wait_for_task


def execute_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []

    for step in plan.get("steps", []):
        title = step.get("title")
        tool = step.get("tool")
        action = step.get("action")
        params = step.get("params", {})

        if (not tool or not action) and "." in step.get("action", ""):
            tool, action = step["action"].split(".", 1)

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

        if (
            tool == "proxmox_action"
            and result.get("ok")
            and isinstance(result.get("data"), str)
            and result["data"].startswith("UPID:")
        ):
            push("Guardian", "Waiting for Proxmox task...", "running")

            task = wait_for_task(
                params.get("node"),
                result["data"],
            )

            result["task"] = task

            if not task.get("ok"):
                err = (task.get("error", "") or task.get("status", "")).lower()

                if "timeout" in err:
                    result["recovery"] = {
                        "title": "Force Reset VM",
                        "tool": "proxmox_action",
                        "action": "reset",
                        "params": params,
                        "reason": "Graceful reboot timed out.",
                    }

                elif "lock" in err:
                    result["recovery"] = {
                        "title": "Retry Later",
                        "tool": None,
                        "action": None,
                        "params": {},
                        "reason": "VM is locked.",
                    }

            if task.get("ok"):
                push("Guardian", "Task completed successfully", "success")
            else:
                push(
                    "Guardian",
                    f"Task failed: {task.get('error', task.get('status'))}",
                    "error",
                )

        results.append({
            "step": step.get("step"),
            "title": title,
            "tool": tool,
            "action": action,
            "params": params,
            "result": result,
        })

        if result.get("ok"):
            push("Executor", f"Completed: {title}", "success")
        else:
            push("Executor", f"Failed: {title}", "error")
            break

    success = all(
        r.get("result", {}).get("ok", False)
        for r in results
    )

    return {
        "ok": success,
        "steps": results,
    }
