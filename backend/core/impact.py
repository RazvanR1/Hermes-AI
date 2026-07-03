from collections import deque

def _adj(graph):
    adj = {}
    for e in graph.get("edges", []):
        adj.setdefault(e["target"], []).append(e["source"])
    return adj

def impacted(component, graph):
    adj = _adj(graph)
    seen = set()
    q = deque([component])
    affected = []

    while q:
        node = q.popleft()
        for nxt in adj.get(node, []):
            if nxt in seen:
                continue
            seen.add(nxt)
            affected.append(nxt)
            q.append(nxt)

    return affected

def analyze(component, ctx):
    graph = ctx.get("graph", {})
    affected = impacted(component, graph)

    severity = "LOW"
    if len(affected) > 20:
        severity = "CRITICAL"
    elif len(affected) > 10:
        severity = "HIGH"
    elif len(affected) > 5:
        severity = "MEDIUM"

    return {
        "mode": "impact_v1",
        "component": component,
        "affected": affected,
        "count": len(affected),
        "severity": severity,
    }
