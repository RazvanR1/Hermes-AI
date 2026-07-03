from core.router import route
from brain import context
from brain import planner
from brain import executor
from brain import reasoner


def _target(request: str):
    q = (request or "").lower()

    aliases = {
        "truenas": "truenas",
        "docker": "docker",
        "opnsense": "opnsense",
        "firewall": "opnsense",
        "plex": "container:plex",
        "immich": "container:immich_server",
        "frigate": "container:frigate",
        "radarr": "container:radarr",
        "sonarr": "container:sonarr",
        "qbittorrent": "container:qbittorrent",
        "proxmox": "proxmox",
        "home assistant": "homeassistant",
        "homeassistant": "homeassistant",
    }

    for key, value in aliases.items():
        if key in q:
            return value

    return None


def _is_rootcause(request: str):
    q = (request or "").lower()
    return any(x in q for x in ["de ce", "cauza", "cauză", "root cause", "nu merge", "problema"])


def _is_impact(request: str):
    q = (request or "").lower()
    return any(x in q for x in ["impact", "afecteaza", "afectează", "ce se întâmplă dacă", "ce se intampla daca", "dacă opresc", "daca opresc"])




def _is_autonomy(request: str):
    q = (request or "").lower()
    return any(x in q for x in [
        "autonomy",
        "autonomous",
        "ce a făcut hermes",
        "ce a facut hermes",
        "ce a reparat hermes",
        "hermes status",
        "self heal",
        "autoheal",
    ])



def _is_decision(request: str):
    q = (request or "").lower()
    return any(x in q for x in [
        "pot face update",
        "pot actualiza",
        "este sigur",
        "e sigur",
        "safe update",
        "update la proxmox",
        "actualizez proxmox",
    ])

def handle(request: str = ""):
    routing = route(request)
    ctx = context.build()

    target = _target(request)


    if _is_decision(request):
        from core import decision

        action = "proxmox.update"
        data = decision.decide(action, ctx)

        return {
            "mode": "brain_decision_v1",
            "request": request,
            "intent": "decision",
            "action": action,
            "decision": data,
            "response": _format_decision(data),
            "routing": routing,
        }

    if _is_rootcause(request):
        from core import rootcause
        from brain.formatter import format_rootcause

        rc = rootcause.explain(target or "homelab", ctx)
        return {
            "mode": "brain_rootcause_v1",
            "request": request,
            "intent": "rootcause",
            "target": target,
            "rootcause": rc,
            "response": format_rootcause(rc),
            "routing": routing,
        }


    if _is_autonomy(request):
        from core import autonomy

        data = autonomy.status()

        return {
            "mode": "brain_autonomy_v1",
            "request": request,
            "intent": "autonomy",
            "autonomy": data,
            "response": str(data),
            "routing": routing,
        }

    if _is_impact(request):
        from core import impact

        component = target or "homelab"
        result = impact.analyze(component, ctx)
        return {
            "mode": "brain_impact_v1",
            "request": request,
            "intent": "impact",
            "target": component,
            "impact": result,
            "response": _format_impact(result),
            "routing": routing,
        }

    plan = planner.build_plan(request, routing, ctx)
    raw = executor.execute(plan, ctx)
    answer = reasoner.summarize(raw)
    answer["routing"] = routing
    return answer


def _format_impact(result):
    lines = []
    lines.append("⚠ Impact Analysis")
    lines.append("")
    lines.append(f"Componentă: {result.get('component')}")
    lines.append(f"Severitate: {result.get('severity')}")
    lines.append(f"Servicii afectate: {result.get('count')}")
    lines.append("")

    affected = result.get("affected", [])
    if affected:
        lines.append("Afectate:")
        for item in affected[:25]:
            lines.append(f"  • {item}")
        if len(affected) > 25:
            lines.append(f"  • ... încă {len(affected) - 25}")

    return "\n".join(lines)


def _format_decision(data):
    allowed = data.get("allowed")
    lines = []

    if allowed:
        lines.append("✅ Decizie Hermes: DA")
    else:
        lines.append("❌ Decizie Hermes: NU")

    lines.append("")
    lines.append(f"Acțiune: {data.get('action')}")
    lines.append(f"Risc: {data.get('risk')}")
    lines.append("")

    reasons = data.get("reasons") or []
    if reasons:
        lines.append("Motive:")
        for r in reasons:
            lines.append(f"  • {r}")
        lines.append("")

    recs = data.get("recommendations") or []
    if recs:
        lines.append("Recomandări:")
        for item in recs[:5]:
            lines.append(
                f"  • {item.get('provider','unknown').upper()}: {item.get('recommendation')}"
            )

    return "\n".join(lines)
