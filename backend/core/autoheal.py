import os

def enabled():
    return os.getenv("HERMES_AUTOHEAL_DOCKER", "0") in ("1", "true", "yes", "on")

def docker_autoheal():
    result = {
        "mode": "docker_autoheal_v1",
        "enabled": enabled(),
        "checked": False,
        "actions": [],
    }

    if not enabled():
        return result

    from providers.docker import client as docker
    from core import actions

    containers = docker.ps()
    result["checked"] = True

    for c in containers:
        name = c.get("name")
        state = c.get("state")

        if state != "exited":
            continue

        r = actions.execute(
            "docker.start",
            target=name,
            confirmed=True,
            ctx={"truenas": "healthy", "critical_incidents": False},
        )

        result["actions"].append({
            "container": name,
            "state": state,
            "result": r,
        })

    return result

def run():
    return {
        "docker": docker_autoheal()
    }
