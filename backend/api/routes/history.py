from fastapi import APIRouter
from api.response import ok
from history.history import list_all, get, clear

router = APIRouter()

@router.get("/history")
def history_list():
    return ok(list_all(), mode="mission_history_v1")

@router.get("/history/{mission_id}")
def history_get(mission_id: str):
    return ok(get(mission_id), mode="mission_history_v1")

@router.delete("/history")
def history_clear():
    clear()
    return ok({"status": "cleared"}, mode="mission_history_v1")
