"""
third_arm.api.schemas.telemetry
─────────────────────────────────────────────────────────────────────────────
Telemetry frame schema — pushed over WebSocket at regular intervals.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from third_arm.core.clock import now_iso


class EEPosition(BaseModel):
    """End-effector Cartesian position (mm, arm-local frame)."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class TelemetryFrame(BaseModel):
    """Real-time telemetry snapshot from the arm."""

    type: Literal["telemetry"] = "telemetry"
    ts: str = Field(default_factory=now_iso)
    session_id: str | None = None
    arm_state: str = "idle"
    joint_angles_deg: list[float] = Field(default_factory=lambda: [0.0] * 6)
    ee_position_mm: EEPosition = Field(default_factory=EEPosition)
    gripper_pct: float = Field(0.0, ge=0.0, le=100.0, description="Gripper open %")
    mock: bool = True
