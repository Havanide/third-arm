"""GET /status — current arm state and session info."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from third_arm.api.deps import get_session_service, get_state_machine
from third_arm.core.clock import now_iso, uptime_s
from third_arm.core.settings import get_settings
from third_arm.domain.session_service import SessionService
from third_arm.domain.state_machine import StateMachine

router = APIRouter(tags=["status"])


@router.get("/status")
async def get_status(
    sm: StateMachine = Depends(get_state_machine),
    sessions: SessionService = Depends(get_session_service),
) -> dict:
    """Return a snapshot of the arm state and active session (if any)."""
    cfg = get_settings()
    active = sessions.active
    return {
        "ts": now_iso(),
        "arm_state": sm.state.value,
        "session_id": active.session_id if active else None,
        "uptime_s": round(uptime_s(), 2),
        "mock_mode": cfg.mock_hardware,
    }
