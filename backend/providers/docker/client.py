import subprocess
import json
from core.config import config

def ssh_target():
    return config.get("DOCKER_SSH_TARGET", "root@192.168.1.200")

def run(cmd):
    full = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", ssh_target(), cmd]
    p = subprocess.run(full, capture_output=True, text=True, timeout=30)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip())
    return p.stdout.strip()

def ps():
    out = run("docker ps -a --format '{{json .}}'")
    result = []
    for line in out.splitlines():
        if not line.strip():
            continue
        c = json.loads(line)
        result.append({
            "name": c.get("Names"),
            "image": c.get("Image"),
            "status": c.get("Status"),
            "state": c.get("State"),
            "ports": c.get("Ports"),
        })
    return result

def stats():
    out = run("docker stats --no-stream --format '{{json .}}'")
    return [json.loads(line) for line in out.splitlines() if line.strip()]

def images():
    out = run("docker images --format '{{json .}}'")
    return [json.loads(line) for line in out.splitlines() if line.strip()]

def info():
    return run("docker info")

def logs(container, tail=100):
    return run(f"docker logs --tail {int(tail)} {container}")

def restart(container):
    return run(f"docker restart {container}")

def start(container):
    return run(f"docker start {container}")

def stop(container):
    return run(f"docker stop {container}")

def compose_ls():
    return run("docker compose ls 2>/dev/null || true")

def inspect(container):
    return json.loads(run(f"docker inspect {container}"))

def exec(container, command):
    return run(f"docker exec {container} {command}")

def pull(image):
    return run(f"docker pull {image}")

def remove(container):
    return run(f"docker rm -f {container}")

def networks():
    out = run("docker network ls --format '{{json .}}'")
    return [json.loads(x) for x in out.splitlines() if x.strip()]

def volumes():
    out = run("docker volume ls --format '{{json .}}'")
    return [json.loads(x) for x in out.splitlines() if x.strip()]
