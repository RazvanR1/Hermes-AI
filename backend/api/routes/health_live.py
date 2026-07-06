from fastapi import APIRouter
from api.response import ok
from inventory.health import calculate_health

router = APIRouter()

@router.get("/health/live")
def live():
    return ok(
        calculate_health(),
        mode="health_v2"
    )
