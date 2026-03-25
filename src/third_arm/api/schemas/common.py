"""
third_arm.api.schemas.common
─────────────────────────────────────────────────────────────────────────────
Shared response envelope and utility schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from third_arm.core.clock import now_iso


class OkResponse(BaseModel):
    """Generic success acknowledgement."""

    ok: bool = True
    ts: str = Field(default_factory=now_iso)
    message: str = "ok"


class ErrorResponse(BaseModel):
    """Generic error response body."""

    ok: bool = False
    code: str
    message: str
    ts: str = Field(default_factory=now_iso)
