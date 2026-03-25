"""
third_arm.api.schemas.events
─────────────────────────────────────────────────────────────────────────────
WebSocket push event schemas.
All events share a ``type`` discriminator field.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from third_arm.core.clock import now_iso


class StateTransitionEvent(BaseModel):
    """Emitted when the arm state machine transitions."""

    type: Literal["state_transition"] = "state_transition"
    ts: str = Field(default_factory=now_iso)
    from_state: str
    to_state: str
    trigger: str


class SessionEvent(BaseModel):
    """Emitted on session lifecycle changes."""

    type: Literal["session_event"] = "session_event"
    ts: str = Field(default_factory=now_iso)
    event: str  # started | stopped | handover_complete | handover_aborted
    session_id: str


class FaultEvent(BaseModel):
    """Emitted when a fault or warning occurs."""

    type: Literal["fault"] = "fault"
    ts: str = Field(default_factory=now_iso)
    code: str
    message: str
    severity: str = "error"  # warning | error | critical
