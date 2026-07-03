from core import policy

try:
    from providers.docker import client as docker
except Exception:
    docker = None

try:
    from providers.proxmox import client as proxmox
except Exception:
    proxmox = None

try:
    from providers.homeassistant import client as ha
except Exception:
    ha = None

try:
    from providers.opnsense import client as opnsense
except Exception:
    opnsense = None


def plan(request: str = ""):
    q = (request or "").lower()
    actions = []

    if "docker" in q or "plex" in q or "container" in q:
        actions.append({
            "action": "docker.inspect",
            "label": "Verifică containerele Docker",
            "policy": policy.classify("docker.inspect"),
            "risk": "low",
            "provider": "docker",
        })

    if "restart" in q or "reporne" in q:
        if "docker" in q or "plex" in q or "container" in q:
            actions.append({
                "action": "docker.restart",
                "label": "Restart container Docker",
                "policy": policy.classify("docker.restart"),
                "risk": "medium",
                "provider": "docker",
                "requires_target": True,
            })

    if "proxmox" in q and ("update" in q or "actualiz" in q):
        actions.append({
            "action": "proxmox.check_updates",
            "label": "Verifică update-urile Proxmox",
            "policy": policy.classify("proxmox.check_updates"),
            "risk": "low",
            "provider": "proxmox",
        })

    if "home assistant" in q or "ha" in q:
        actions.append({
            "action": "homeassistant.check_updates",
            "label": "Verifică update-urile Home Assistant",
            "policy": policy.classify("homeassistant.check_updates"),
            "risk": "low",
            "provider": "homeassistant",
        })

    if "opnsense" in q or "firewall" in q:
        actions.append({
            "action": "opnsense.check_updates",
            "label": "Verifică update-urile OPNsense",
            "policy": policy.classify("opnsense.check_updates"),
            "risk": "low",
            "provider": "opnsense",
        })

    if not actions:
        actions.append({
            "action": "homelab.audit",
            "label": "Audit general homelab",
            "policy": "SAFE",
            "risk": "low",
            "provider": "hermes",
        })

    return {
        "mode": "action_plan_v1",
        "request": request,
        "actions": actions,
        "summary": {
            "total": len(actions),
            "safe": len([a for a in actions if a.get("policy") == "SAFE"]),
            "confirm": len([a for a in actions if a.get("policy") == "CONFIRM"]),
            "dangerous": len([a for a in actions if a.get("policy") == "DANGEROUS"]),
        },
    }


def _build_policy_context():
    ctx = {
        "truenas": "healthy",
        "critical_incidents": False,
    }

    try:
        from core import incidents
        open_items = incidents.list_open()
        for item in open_items:
            sev = item.get("severity")
            title = str(item.get("title", "")).lower()
            provider = str(item.get("provider", "")).lower()

            if sev == "critical":
                ctx["critical_incidents"] = True

            if provider == "truenas" and any(x in title for x in ["degraded", "removed", "faulted", "critical"]):
                ctx["truenas"] = "degraded"
    except Exception:
        pass

    return ctx


def _policy_action(action_name):
    aliases = {
        "proxmox.apply_updates": "proxmox.update",
        "proxmox.update": "proxmox.update",
        "truenas.apply_updates": "truenas.update",
        "truenas.update": "truenas.update",
        "docker.update": "docker.update",
    }
    return aliases.get(action_name, action_name)


def execute(action_name: str, target: str = None, confirmed: bool = False, ctx: dict = None):
    ctx = ctx or _build_policy_context()

    decision = policy.can_execute(_policy_action(action_name), ctx)
    if not decision.get("allowed"):
        return {
            "executed": False,
            "action": action_name,
            "policy": decision.get("policy"),
            "reason": decision.get("reason"),
            "blocked_by_policy": True,
            "context": ctx,
        }

    gate = policy.classify(action_name)

    if not policy.allowed(action_name, confirmed=confirmed):
        return {
            "executed": False,
            "action": action_name,
            "policy": gate,
            "reason": "Acțiunea necesită confirmare.",
            "needs_confirmation": gate in ("CONFIRM", "DANGEROUS"),
            "context": ctx,
        }

    if action_name == "docker.inspect":
        if docker is None:
            return _provider_error(action_name, "docker")
        return {"executed": True, "action": action_name, "result": docker.ps()}

    if action_name == "docker.restart":
        if docker is None:
            return _provider_error(action_name, "docker")
        if not target:
            return {"executed": False, "action": action_name, "reason": "Lipsește target container."}
        return {"executed": True, "action": action_name, "target": target, "result": docker.restart(target)}

    if action_name == "proxmox.check_updates":
        if proxmox is None:
            return _provider_error(action_name, "proxmox")
        return {"executed": True, "action": action_name, "result": proxmox.updates()}

    if action_name == "homeassistant.check_updates":
        if ha is None:
            return _provider_error(action_name, "homeassistant")
        return {"executed": True, "action": action_name, "result": ha.updates()}

    if action_name == "opnsense.check_updates":
        if opnsense is None:
            return _provider_error(action_name, "opnsense")
        return {"executed": True, "action": action_name, "result": opnsense.summary()}

    return {"executed": False, "action": action_name, "reason": "Acțiune necunoscută."}

def _provider_error(action, provider):
    return {
        "executed": False,
        "action": action,
        "provider": provider,
        "reason": f"Providerul {provider} nu este disponibil.",
    }
