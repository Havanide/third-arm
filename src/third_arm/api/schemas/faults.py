"""
third_arm.api.schemas.faults
─────────────────────────────────────────────────────────────────────────────
Fault / error response schemas and fault code catalogue.

TODO: expand fault codes as hardware integration proceeds.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from third_arm.core.clock import now_iso


class FaultResponse(BaseModel):
    """API response body for fault conditions."""

    ok: bool = False
    fault_code: str
    message: str
    severity: str = "error"
    ts: str = Field(default_factory=now_iso)
    recoverable: bool = True
    suggested_action: str = "Check logs and retry"


# ── Fault code constants ──────────────────────────────────────────────────────
class FaultCode:
    INVALID_TRANSITION = "INVALID_TRANSITION"
    ARM_NOT_READY      = "ARM_NOT_READY"
    SESSION_CONFLICT   = "SESSION_CONFLICT"
    NO_ACTIVE_SESSION  = "NO_ACTIVE_SESSION"
    HARDWARE_ERROR     = "HARDWARE_ERROR"
    ESTOP              = "ESTOP"
    CONFIG_ERROR       = "CONFIG_ERROR"
    INTERNAL_ERROR     = "INTERNAL_ERROR"
