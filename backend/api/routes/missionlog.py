from fastapi import APIRouter
from api.response import ok
from missionlog.log import get, clear

router = APIRouter()

@router.get("/missionlog")
def mission_log():
    return ok(get(), mode="mission_log_v1")

@router.delete("/missionlog")
def clear_log():
    clear()
    return ok({"status": "cleared"})
