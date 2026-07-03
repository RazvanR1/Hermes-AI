REGISTRY = {}

def register(name, provider=None, capabilities=None):
    REGISTRY[name] = {"provider": provider, "capabilities": capabilities or []}

def find_by_capability(capability):
    return {name: item for name, item in REGISTRY.items() if capability in item.get("capabilities", [])}

def all():
    return REGISTRY
