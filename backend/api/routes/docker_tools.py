from fastapi import APIRouter
from pydantic import BaseModel
from api.response import ok
from tools.docker import docker_tool

router = APIRouter()

class DockerRequest(BaseModel):
    action: str

@router.post("/tools/docker")
def docker_action(req: DockerRequest):
    return ok(docker_tool.execute(req.action))
