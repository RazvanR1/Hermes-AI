from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from operator_v8 import operator_chat


router = APIRouter(
    prefix="/operator/v8",
    tags=["operator-v8"],
)


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=4000,
    )
    source: str = Field(
        default="api",
        max_length=100,
    )
    user: str = Field(
        default="local",
        max_length=100,
    )


@router.get("/health")
def health():
    return {
        "ok": True,
        "module": "operator-v8",
        "version": (
            "v8.0.0-alpha5.4-brain-integration"
        ),
        "brain": {
            "enabled": True,
            "migration_mode": "incremental",
        },
    }


@router.post("/chat")
def chat(body: ChatRequest):
    return operator_chat(
        body.message,
        source=body.source,
        user=body.user,
    )
