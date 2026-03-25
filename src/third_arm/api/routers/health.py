"""GET /health — liveness check."""

from __future__ import annotations

from fastapi import APIRouter

from third_arm.api.schemas.common import OkResponse
from third_arm.core.clock import now_iso

router = APIRouter(tags=["health"])


@router.get("/health", response_model=OkResponse)
async def get_health() -> dict:
    """Liveness probe — always returns 200 if the process is alive."""
    return {"ok": True, "ts": now_iso(), "message": "ok"}
