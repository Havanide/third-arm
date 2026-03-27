"""
third_arm.api.schemas.commands
─────────────────────────────────────────────────────────────────────────────
Request and response schemas for operator commands.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class SessionStartRequest(BaseModel):
    """Body for POST /session/start."""

    operator_id: str = Field("operator", description="Operator identifier")
    object_id: str | None = Field(None, description="Object to hand over (optional at start)")
    slot_id: str | None = Field(None, description="Slot to pick from (optional at start)")
    notes: str = Field("", description="Free-text session notes")


class HandoverRequestBody(BaseModel):
    """Body for POST /handover/request."""

    object_id: str = Field(..., description="Object catalogue ID")
    slot_id: str = Field(..., description="Source slot ID")


class SessionResponse(BaseModel):
    """Response body for POST /session/start."""

    session_id: str
    started_at: str
    operator_id: str


class SessionStopResponse(BaseModel):
    """Response body for POST /session/stop."""

    session_id: str
    stopped_at: str
    status: str


class HandoverResponse(BaseModel):
    """Response body for POST /handover/request."""

    handover_id: str
    object_id: str
    slot_id: str
    completed_at: str
    status: str
