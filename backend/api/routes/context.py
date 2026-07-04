from fastapi import APIRouter
from api.response import ok
from brain import context_engine

router = APIRouter()

@router.get("/context")
def get_context():
    return ok(
        context_engine.build("dashboard"),
        mode="context_v1",
    )
