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
from third_arm.domain.contracts import BundleWriterABC
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
    bundle_path: str | None = None

    @property
    def is_active(self) -> bool:
        return self.stopped_at is None


class SessionService:
    """Manages the single active session.

    Intended to be a singleton injected via FastAPI dependency.

    Args:
        bundle_writer: Port implementation for session bundle logging.
    """

    def __init__(self, bundle_writer: BundleWriterABC) -> None:
        self._active: Session | None = None
        self._bundle_writer = bundle_writer

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

        Opens a bundle directory before creating the session object.
        If the bundle cannot be opened the session is NOT created.

        Raises:
            SessionAlreadyActiveError: if a session is already running.
            RuntimeError: if the bundle writer fails to open.
        """
        allowed, reason = can_start_session(
            self._active.session_id if self._active else None
        )
        if not allowed:
            raise SessionAlreadyActiveError(self._active.session_id)  # type: ignore[union-attr]

        session_id = new_session_id()

        try:
            self._bundle_writer.open_session(
                session_id,
                metadata={
                    "operator_id": operator_id,
                    "object_id": object_id,
                    "slot_id": slot_id,
                    "notes": notes,
                },
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to open bundle for session {session_id}") from exc

        session = Session(
            session_id=session_id,
            operator_id=operator_id,
            object_id=object_id,
            slot_id=slot_id,
            started_at=now_iso(),
            notes=notes,
            bundle_path=str(self._bundle_writer.bundle_dir),
        )
        self._active = session

        self._bundle_writer.write_trace_event({
            "event": "session_started",
            "session_id": session_id,
            "operator_id": operator_id,
            "object_id": object_id,
            "slot_id": slot_id,
        })

        return session

    def stop(self) -> Session:
        """Stop the active session.

        Writes a trace event and closes the bundle before returning.

        Raises:
            NoActiveSessionError: if no session is running.
        """
        if self._active is None:
            raise NoActiveSessionError()

        self._bundle_writer.write_trace_event({
            "event": "session_stopped",
            "session_id": self._active.session_id,
        })

        self._active.stopped_at = now_iso()
        completed = self._active
        self._active = None
        self._bundle_writer.close_session()
        return completed

    def require_active(self) -> Session:
        """Return the active session or raise NoActiveSessionError."""
        if self._active is None:
            raise NoActiveSessionError()
        return self._active
