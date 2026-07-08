from datetime import datetime, timezone
from typing import Dict, Any
import time

from mission_store_v8 import get_mission, update_mission
from actions_v8_runner import run_registered_action

try:
    from mission_events_v8 import (
        mission_approved,
        mission_running,
        mission_completed,
        mission_failed,
        step_started,
        step_finished,
    )
except Exception:
    mission_approved = mission_running = mission_completed = mission_failed = None
    step_started = step_finished = None


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _log(mission: Dict[str, Any], level: str, message: str, data: Dict[str, Any] | None = None):
    mission.setdefault("logs", []).append({
        "time": now(),
        "level": level,
        "message": message,
        "data": data or {},
    })


def _verify_step(step: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    action = step.get("action")
    params = step.get("params") or {}

    if not result.get("ok"):
        return {"ok": False, "method": "result-ok", "message": "Action result is not ok"}

    if action and action.startswith("proxmox.vm.") and action != "proxmox.vm.status":
        time.sleep(3)
        verify = run_registered_action("proxmox.vm.status", {
            "node": params.get("node", "proxmox"),
            "vmid": params.get("vmid"),
        })
        return {
            "ok": bool(verify.get("ok")),
            "method": "proxmox.vm.status",
            "result": verify,
        }

    if action and action.startswith("proxmox.lxc.") and action != "proxmox.lxc.status":
        time.sleep(3)
        verify = run_registered_action("proxmox.lxc.status", {
            "node": params.get("node", "proxmox"),
            "vmid": params.get("vmid"),
        })
        return {
            "ok": bool(verify.get("ok")),
            "method": "proxmox.lxc.status",
            "result": verify,
        }

    return {"ok": True, "method": "result-ok"}


def execute_approved_steps(mission_id: str) -> Dict[str, Any]:
    mission = get_mission(mission_id)
    if not mission:
        return {"ok": False, "error": "Mission not found", "mission_id": mission_id}

    mission["status"] = "running"
    mission.setdefault("execution", {})
    mission["execution"]["mode"] = "approved-execution"
    mission["execution"]["started_at"] = now()

    _log(mission, "info", "Mission execution started")

    if mission_running:
        mission_running(mission_id)

    executed = []
    failed = []
    skipped = []

    for step in mission.get("steps", []):
        status = step.get("status")
        approved = step.get("approved")
        risk = step.get("risk")
        blocked = step.get("blocked")

        if blocked or risk == "BLOCK":
            step["status"] = "blocked"
            skipped.append(step)
            continue

        if risk == "CONFIRM" and not approved:
            if step.get("status") != "done":
                step["status"] = "waiting_confirmation"
            skipped.append(step)
            continue

        if status == "done":
            skipped.append(step)
            continue

        if not approved and risk != "SAFE":
            skipped.append(step)
            continue

        action = step.get("action")
        params = step.get("params") or {}

        step["status"] = "running"
        step["started_at"] = now()
        _log(mission, "info", f"Step started: {step.get('id')}", {"action": action, "params": params})

        if step_started:
            step_started(mission_id, step.get("id"), action)

        result = run_registered_action(action, params)
        verify = _verify_step(step, result)

        step["result"] = result
        step["verification"] = verify
        step["finished_at"] = now()

        ok = bool(result.get("ok")) and bool(verify.get("ok"))

        if ok:
            step["status"] = "done"
            executed.append(step)
        else:
            step["status"] = "failed"
            failed.append(step)

        _log(mission, "info" if ok else "error", f"Step finished: {step.get('id')} status={step['status']}", {
            "action": action,
            "ok": ok,
            "result": result,
            "verification": verify,
        })

        if step_finished:
            step_finished(
                mission_id,
                step.get("id"),
                action=action,
                ok=ok,
                data={"verification": verify},
            )

        if not ok:
            break

    waiting = [
        s for s in mission.get("steps", [])
        if s.get("status") == "waiting_confirmation"
    ]

    if failed:
        mission["status"] = "failed"
        if mission_failed:
            mission_failed(mission_id, error="One or more steps failed", data={"failed": len(failed)})
    elif waiting:
        mission["status"] = "waiting_confirmation"
    else:
        mission["status"] = "completed"
        if mission_completed:
            mission_completed(mission_id, data={"executed": len(executed)})

    mission["execution"].update({
        "finished_at": now(),
        "executed_count": len(executed),
        "failed_count": len(failed),
        "skipped_count": len(skipped),
        "waiting_confirmation_count": len(waiting),
    })

    _log(mission, "info", f"Mission execution finished: {mission['status']}")
    update_mission(mission)

    return {
        "ok": not bool(failed),
        "mission": mission,
        "executed_count": len(executed),
        "failed_count": len(failed),
        "skipped_count": len(skipped),
        "waiting_confirmation_count": len(waiting),
    }
