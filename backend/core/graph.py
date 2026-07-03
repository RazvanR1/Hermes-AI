from collections import defaultdict, deque
from core.models import Node, Edge

class HomelabGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id, name, kind, provider="unknown", status="unknown", metadata=None):
        node_id = str(node_id)
        self.nodes[node_id] = Node(node_id, str(name), str(kind), str(provider), str(status or "unknown"), metadata or {})
        return self.nodes[node_id]

    def connect(self, source, target, relation, metadata=None):
        source, target = str(source), str(target)
        if source not in self.nodes:
            self.add_node(source, source, "unknown")
        if target not in self.nodes:
            self.add_node(target, target, "unknown")
        edge = Edge(source, target, str(relation), metadata or {})
        self.edges.append(edge)
        return edge

    def find(self, query):
        q = str(query).lower()
        return [n.to_dict() for n in self.nodes.values() if q in n.id.lower() or q in n.name.lower() or q in n.kind.lower()]

    def dependents(self, node_id, max_depth=5):
        return self._walk(str(node_id), "in", max_depth)

    def dependencies(self, node_id, max_depth=5):
        return self._walk(str(node_id), "out", max_depth)

    def impact(self, node_id):
        affected = self.dependents(node_id, 5)
        critical = [x for x in affected if x.get("kind") in ("vm", "lxc", "container", "service", "storage", "backup")]
        return {"target": str(node_id), "affected_count": len(affected), "affected": affected, "critical": critical}

    def to_dict(self):
        return {"nodes": [n.to_dict() for n in self.nodes.values()], "edges": [e.to_dict() for e in self.edges], "counts": {"nodes": len(self.nodes), "edges": len(self.edges)}}

    def _walk(self, start, direction, max_depth):
        seen = {start}
        q = deque([(start, 0)])
        result = []
        index = defaultdict(list)
        for edge in self.edges:
            if direction == "out":
                index[edge.source].append((edge.target, edge))
            else:
                index[edge.target].append((edge.source, edge))
        while q:
            cur, depth = q.popleft()
            if depth >= max_depth:
                continue
            for nxt, edge in index.get(cur, []):
                if nxt in seen:
                    continue
                seen.add(nxt)
                node = self.nodes.get(nxt)
                if node:
                    item = node.to_dict()
                    item["via_relation"] = edge.relation
                    item["depth"] = depth + 1
                    result.append(item)
                    q.append((nxt, depth + 1))
        return result
