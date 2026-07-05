import docker
from typing import Dict, Any
from .base import Tool

class DockerTool(Tool):
    name = "docker"

    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception:
            self.client = None

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        if self.client is None:
            return {
                "ok": False,
                "error": "Docker daemon unavailable."
            }

        try:
            if action == "list_containers":
                containers = []

                for c in self.client.containers.list(all=True):
                    containers.append({
                        "id": c.short_id,
                        "name": c.name,
                        "image": c.image.tags[0] if c.image.tags else "<none>",
                        "status": c.status,
                    })

                return {
                    "ok": True,
                    "count": len(containers),
                    "containers": containers,
                }

            if action == "info":
                info = self.client.info()

                return {
                    "ok": True,
                    "name": info.get("Name"),
                    "containers": info.get("Containers"),
                    "running": info.get("ContainersRunning"),
                    "paused": info.get("ContainersPaused"),
                    "stopped": info.get("ContainersStopped"),
                    "images": info.get("Images"),
                    "driver": info.get("Driver"),
                    "kernel": info.get("KernelVersion"),
                    "os": info.get("OperatingSystem"),
                }

            return {
                "ok": False,
                "error": f"Unknown action '{action}'"
            }

        except Exception as e:
            return {
                "ok": False,
                "error": str(e)
            }

docker_tool = DockerTool()
