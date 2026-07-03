from fastapi import APIRouter
from api.response import ok

router = APIRouter()

@router.get("/health")
def health():
    return ok({"service": "Hermes", "status": "ok"}, mode="health_v1")
