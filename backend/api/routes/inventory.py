from fastapi import APIRouter
from api.response import ok
from inventory.inventory import inventory

router = APIRouter()

@router.get("/inventory")
def get_inventory():
    return ok(
        inventory.collect(),
        mode="inventory_v1"
    )
