from fastapi import APIRouter

from api.response import ok
from brain import context_engine
from core import reasoning

router = APIRouter()

@router.get("/reasoning")
def get_reasoning():
    ctx = context_engine.build("dashboard")

    return ok(
        reasoning.explain(ctx),
        mode="reasoning_v1",
    )
