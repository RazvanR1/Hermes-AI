def _find_node(graph, query):
    q = (query or "").lower()
    for node in graph.get("nodes", []):
        if q in node.get("id", "").lower() or q in node.get("name", "").lower():
            return node
    return None


def _incoming(graph, node_id):
    return [e for e in graph.get("edges", []) if e.get("source") == node_id or e.get("target") == node_id]


def _open_incidents_by_provider(incidents):
    out = {}
    for item in incidents or []:
        provider = (item.get("provider") or "").lower()
        out.setdefault(provider, []).append(item)
    return out


def explain(entity, ctx):
    graph = ctx.get("graph") or {}
    incidents = ((ctx.get("incidents") or {}).get("open")) or []
    policies = ctx.get("policies") or []

    node = _find_node(graph, entity)
    incident_map = _open_incidents_by_provider(incidents)

    chain = []
    evidence = []
    confidence = 30
    recommendation = "Nu am suficiente date pentru o cauză clară."

    if node:
        chain.append({
            "step": "entity_found",
            "node": node,
        })
        confidence += 20

        for edge in _incoming(graph, node.get("id")):
            chain.append({
                "step": "relationship",
                "edge": edge,
            })

    # Heuristic v1: media/docker services often depend on Docker + TrueNAS storage.
    q = (entity or "").lower()
    if any(x in q for x in ["plex", "immich", "radarr", "sonarr", "qbittorrent", "frigate"]):
        chain.extend([
            {"step": "service_layer", "component": "docker"},
            {"step": "storage_layer", "component": "truenas"},
        ])
        evidence.append("Serviciile media folosesc Docker și storage din TrueNAS.")
        confidence += 15

    if "truenas" in incident_map:
        evidence.append("Există incident deschis pe TrueNAS.")
        chain.append({
            "step": "incident",
            "provider": "truenas",
            "items": incident_map["truenas"],
        })
        confidence += 30
        recommendation = "Verifică întâi TrueNAS/pool/storage înainte să repornești serviciile dependente."

    for p in policies:
        if p.get("policy") or p.get("id"):
            evidence.append(f"Policy activă: {p.get('policy') or p.get('id')}")
            confidence += 10

    confidence = min(confidence, 95)

    if not evidence:
        evidence.append("Nu există incidente clare asociate în acest moment.")

    return {
        "mode": "rootcause_v1",
        "entity": entity,
        "root_cause": recommendation,
        "confidence": confidence,
        "evidence": evidence,
        "chain": chain,
    }


def explain_incidents(ctx):
    incidents = ((ctx.get("incidents") or {}).get("open")) or []
    results = []

    for item in incidents:
        provider = item.get("provider") or "unknown"
        results.append(explain(provider, ctx))

    return {
        "mode": "rootcause_incidents_v1",
        "count": len(results),
        "items": results,
    }
