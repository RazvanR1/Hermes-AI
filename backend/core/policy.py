import os
import yaml

POLICY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "policies")
_policies = None

def load_policies(force=False):
    global _policies
    if _policies is not None and not force:
        return _policies

    policies = []
    if not os.path.isdir(POLICY_DIR):
        _policies = []
        return _policies

    for name in sorted(os.listdir(POLICY_DIR)):
        if not name.endswith(".yaml"):
            continue
        with open(os.path.join(POLICY_DIR, name), "r") as f:
            data = yaml.safe_load(f) or {}
        if data.get("enabled", True):
            policies.append(data)

    policies.sort(key=lambda p: p.get("priority", 0), reverse=True)
    _policies = policies
    return policies

def _match(rule, ctx):
    for key, expected in rule.items():
        if ctx.get(key) != expected:
            return False
    return True

def check(ctx):
    violations = []
    for p in load_policies():
        if _match(p.get("when", {}), ctx):
            violations.append({
                "id": p["id"],
                "message": p.get("message"),
                "deny": p.get("deny", []),
                "priority": p.get("priority", 0),
            })
    return violations

def can_execute(action, ctx):
    for item in check(ctx):
        if action in item["deny"]:
            return {
                "allowed": False,
                "policy": item["id"],
                "reason": item["message"],
            }

    return {"allowed": True, "policy": None, "reason": None}


DEFAULT_ACTION_POLICIES = {
    "docker.inspect": "SAFE",
    "docker.restart": "CONFIRM",
    "docker.start": "CONFIRM",
    "docker.stop": "CONFIRM",
    "homeassistant.check_updates": "SAFE",
    "proxmox.check_updates": "SAFE",
    "opnsense.check_updates": "SAFE",
}

def classify(action_name: str):
    return DEFAULT_ACTION_POLICIES.get(action_name, "CONFIRM")

def allowed(action_name: str, confirmed: bool = False):
    gate = classify(action_name)
    if gate == "SAFE":
        return True
    if gate in ("CONFIRM", "DANGEROUS"):
        return bool(confirmed)
    return False
