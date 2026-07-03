from fastapi import APIRouter
from api.response import ok
from brain import dashboard

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    return ok(dashboard.build(), mode="dashboard_v1")
