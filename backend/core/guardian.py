from datetime import datetime, timezone
import json
import os

try:
    from core import inventory as inventory_core
    from core import incidents as incident_core
    from core import reasoning as reasoning_core
    from core.relationships import build_from_inventory
    from core import actions as action_core
except Exception:
    inventory_core = None
    incident_core = None
    reasoning_core = None
    build_from_inventory = None
    action_core = None

STATE_PATH = os.getenv("HERMES_GUARDIAN_STATE", "/home/hermes/.hermes/homelab/guardian-state.json")

def _now():
    return datetime.now(timezone.utc).isoformat()

def run_once(auto_safe=False):
    report = {
        "mode": "guardian_v1",
        "timestamp": _now(),
        "auto_safe": bool(auto_safe),
        "ok": True,
        "errors": [],
        "inventory": None,
        "graph": None,
        "incidents": None,
        "reasoning": None,
        "actions": [],
    }

    try:
        if inventory_core:
            report["inventory"] = inventory_core.build_inventory()
        else:
            report["errors"].append("inventory_core not available")
    except Exception as e:
        report["errors"].append(f"inventory error: {e}")

    try:
        if report["inventory"] and build_from_inventory:
            graph = build_from_inventory(report["inventory"])
            report["graph"] = graph.to_dict()
    except Exception as e:
        report["errors"].append(f"graph error: {e}")

    synthetic = {"critical": [], "warnings": [], "inventory": report.get("inventory")}
    inv = report.get("inventory") or {}

    for warning in inv.get("warnings", []) or []:
        synthetic["warnings"].append(warning)

    components = (inv.get("components") or {}) if isinstance(inv, dict) else {}
    for name, comp in components.items():
        if isinstance(comp, dict) and not comp.get("ok", True):
            synthetic["warnings"].append(f"{name} provider unavailable: {comp.get('error') or comp.get('status')}")

    try:
        if incident_core:
            report["incidents"] = incident_core.sync_from_report(synthetic)
    except Exception as e:
        report["errors"].append(f"incidents error: {e}")

    try:
        if reasoning_core:
            report["reasoning"] = reasoning_core.analyze({
                "inventory": report.get("inventory"),
                "incidents": report.get("incidents"),
                "score": None,
            })
    except Exception as e:
        report["errors"].append(f"reasoning error: {e}")

    if auto_safe and action_core:
        for action_name in ["proxmox.check_updates", "homeassistant.check_updates", "opnsense.check_updates"]:
            try:
                report["actions"].append(action_core.execute(action_name, confirmed=False))
            except Exception as e:
                report["actions"].append({"executed": False, "action": action_name, "error": str(e)})

    try:
        from core import autoheal
        report["autoheal"] = autoheal.run()
    except Exception as e:
        report["errors"].append(f"autoheal error: {e}")

    if report["errors"]:
        report["ok"] = False

    _save_state(report)
    return report

def status():
    state = _load_state()
    open_incidents = []
    if incident_core:
        try:
            open_incidents = incident_core.list_open()
        except Exception:
            open_incidents = []
    return {
        "mode": "guardian_status_v1",
        "state_path": STATE_PATH,
        "last_run": state,
        "open_incidents": open_incidents,
    }

def _save_state(report):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

def _load_state():
    try:
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        return {"error": str(e)}
