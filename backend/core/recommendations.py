def _impact_count(component, ctx):
    try:
        from core import impact
        return impact.analyze(component, ctx).get("count", 0)
    except Exception:
        return 0


def build(ctx):
    recs = []

    incidents = ((ctx.get("incidents") or {}).get("open")) or []
    inventory = ctx.get("inventory") or {}

    for item in incidents:
        provider = (item.get("provider") or "").lower()
        severity = item.get("severity", "warning")
        title = item.get("title", "")

        score = 50
        if severity == "critical":
            score += 40
        elif severity == "warning":
            score += 20

        impact_count = _impact_count(provider, ctx)
        score += min(impact_count, 40)

        recs.append({
            "priority": score,
            "provider": provider,
            "severity": severity,
            "title": title,
            "impact_count": impact_count,
            "recommendation": item.get("recommendation") or "Verifică incidentul.",
        })

    summary = inventory.get("summary", {})
    if summary.get("docker_exited", 0) > 0:
        recs.append({
            "priority": 85,
            "provider": "docker",
            "severity": "warning",
            "title": f"{summary.get('docker_exited')} containere Docker sunt oprite",
            "impact_count": _impact_count("docker", ctx),
            "recommendation": "Rulează auto-heal sau verifică manual containerele oprite.",
        })

    if summary.get("docker_running", 0) > 0 and summary.get("docker_exited", 0) == 0:
        recs.append({
            "priority": 10,
            "provider": "docker",
            "severity": "info",
            "title": "Docker este sănătos",
            "impact_count": summary.get("docker_running", 0),
            "recommendation": "Nu este necesară intervenție Docker.",
        })

    recs.sort(key=lambda x: x.get("priority", 0), reverse=True)

    return {
        "mode": "recommendations_v1",
        "count": len(recs),
        "items": recs,
    }


def format_report(data):
    lines = ["📋 Recomandări Hermes", ""]

    items = data.get("items", [])
    if not items:
        return "📋 Recomandări Hermes\n\nNu am recomandări momentan."

    for i, item in enumerate(items[:10], 1):
        lines.append(f"{i}. {item.get('provider', 'unknown').upper()}")
        lines.append(f"   Severitate: {item.get('severity')}")
        lines.append(f"   Impact: {item.get('impact_count')} servicii")
        lines.append(f"   Motiv: {item.get('title')}")
        lines.append(f"   Recomandare: {item.get('recommendation')}")
        lines.append("")

    return "\n".join(lines)
