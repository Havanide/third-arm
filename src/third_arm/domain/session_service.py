"""
third_arm.domain.session_service
─────────────────────────────────────────────────────────────────────────────
Session lifecycle management: start / stop / status.

A *session* groups a single handover attempt: it owns an ID, tracks timing,
and gates the bundle logging lifecycle.

Stage 1: operator-triggered only. One session at a time.

TODO: add session persistence (reload on restart).
TODO (Stage 2+): multi-operator / concurrent session support.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from third_arm.core.clock import now_iso
from third_arm.core.errors import NoActiveSessionError, SessionAlreadyActiveError
from third_arm.core.ids import new_session_id
from third_arm.domain.policies import can_start_session


@dataclass
class Session:
    """Runtime session descriptor."""

    session_id: str
    operator_id: str
    object_id: str | None
    slot_id: str | None
    started_at: str
    stopped_at: str | None = None
    notes: str = ""
    handover_ids: list[str] = field(default_factory=list)

    @property
    def is_active(self) -> bool:
        return self.stopped_at is None


class SessionService:
    """Manages the single active session.

    Intended to be a singleton injected via FastAPI dependency.

    TODO: wire to BundleWriter for logging open/close events.
    """

    def __init__(self) -> None:
        self._active: Session | None = None

    @property
    def active(self) -> Session | None:
        return self._active

    def start(
        self,
        *,
        operator_id: str = "operator",
        object_id: str | None = None,
        slot_id: str | None = None,
        notes: str = "",
    ) -> Session:
        """Start a new session.

        Raises:
            SessionAlreadyActiveError: if a session is already running.
        """
        allowed, reason = can_start_session(
            self._active.session_id if self._active else None
        )
        if not allowed:
            raise SessionAlreadyActiveError(self._active.session_id)  # type: ignore[union-attr]

        session = Session(
            session_id=new_session_id(),
            operator_id=operator_id,
            object_id=object_id,
            slot_id=slot_id,
            started_at=now_iso(),
            notes=notes,
        )
        self._active = session
        return session

    def stop(self) -> Session:
        """Stop the active session.

        Raises:
            NoActiveSessionError: if no session is running.
        """
        if self._active is None:
            raise NoActiveSessionError()
        self._active.stopped_at = now_iso()
        completed = self._active
        self._active = None
        return completed

    def require_active(self) -> Session:
        """Return the active session or raise NoActiveSessionError."""
        if self._active is None:
            raise NoActiveSessionError()
        return self._active
