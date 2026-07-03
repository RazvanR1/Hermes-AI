from dataclasses import dataclass, asdict

@dataclass
class Node:
    id: str
    name: str
    kind: str
    provider: str = "unknown"
    status: str = "unknown"
    metadata: dict | None = None

    def to_dict(self):
        data = asdict(self)
        data["metadata"] = data["metadata"] or {}
        return data

@dataclass
class Edge:
    source: str
    target: str
    relation: str
    metadata: dict | None = None

    def to_dict(self):
        data = asdict(self)
        data["metadata"] = data["metadata"] or {}
        return data
