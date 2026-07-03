from core.graph import HomelabGraph

def build_from_inventory(inventory):
    graph = HomelabGraph()
    graph.add_node("homelab", "Homelab", "root", "hermes", "online")
    components = (inventory or {}).get("components", {}) or {}

    for provider in ["proxmox", "docker", "truenas", "homeassistant", "opnsense"]:
        comp = components.get(provider, {}) or {}
        status = "online" if comp.get("ok") else comp.get("status", "unknown")
        graph.add_node(provider, provider, "provider", provider, status, comp)
        graph.connect(provider, "homelab", "part_of")

    prox = components.get("proxmox", {}) or {}
    for vm in prox.get("vms", []) or []:
        node_id = f"vm:{vm.get('id') or vm.get('name')}"
        graph.add_node(node_id, vm.get("name") or node_id, "vm", "proxmox", vm.get("status"), vm)
        graph.connect(node_id, "proxmox", "hosted_on")
        name = str(vm.get("name") or "").lower()
        if "truenas" in name:
            graph.connect("truenas", node_id, "runs_as")
        if "home" in name or "ha" in name:
            graph.connect("homeassistant", node_id, "runs_as")

    for ct in prox.get("lxcs", []) or []:
        node_id = f"lxc:{ct.get('id') or ct.get('name')}"
        graph.add_node(node_id, ct.get("name") or node_id, "lxc", "proxmox", ct.get("status"), ct)
        graph.connect(node_id, "proxmox", "hosted_on")
        if any(x in str(ct.get("name") or "").lower() for x in ["docker", "portainer"]):
            graph.connect("docker", node_id, "runs_on")

    docker = components.get("docker", {}) or {}
    for c in docker.get("containers", []) or []:
        name = c.get("name") or c.get("id") or "container"
        node_id = f"container:{name}"
        graph.add_node(node_id, name, "container", "docker", c.get("status"), c)
        graph.connect(node_id, "docker", "runs_on")
        lname = str(name).lower()
        if any(x in lname for x in ["plex", "immich", "radarr", "sonarr", "qbittorrent", "frigate"]):
            graph.connect(node_id, "truenas", "uses_storage")
            graph.connect(node_id, "opnsense", "uses_network")

    graph.add_node("storage:homecloud", "HomeCloud", "storage", "truenas", "unknown")
    graph.connect("storage:homecloud", "truenas", "provided_by")
    graph.connect("docker", "storage:homecloud", "uses_storage")

    graph.add_node("network:lan", "LAN", "network", "opnsense", "online")
    graph.add_node("network:wan", "WAN", "network", "opnsense", "unknown")
    graph.connect("network:lan", "opnsense", "provided_by")
    graph.connect("network:wan", "opnsense", "provided_by")
    graph.connect("proxmox", "network:lan", "uses_network")
    graph.connect("docker", "network:lan", "uses_network")
    graph.connect("homeassistant", "network:lan", "uses_network")

    return graph
