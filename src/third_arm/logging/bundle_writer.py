"""
third_arm.logging.bundle_writer
─────────────────────────────────────────────────────────────────────────────
Session bundle writer — coordinates manifest, NDJSON trace, and MCAP file.

A *bundle* is a self-contained directory for one session:

    sessions/<session_id>/
        manifest.json          ← session metadata + file index
        session_trace.ndjson   ← human-readable structured event log
        telemetry.mcap         ← binary telemetry (placeholder in Stage 1)

BundleWriter implements BundleWriterABC so it can be swapped out in tests.

TODO: make write_trace_event async (aiofiles).
TODO: add telemetry streaming to McapWriter per-frame.
"""

from __future__ import annotations

import logging
from pathlib import Path

from third_arm.domain.contracts import BundleWriterABC
from third_arm.logging.manifest import close_manifest, write_manifest
from third_arm.logging.mcap_writer import McapWriter
from third_arm.logging.trace_writer import TraceWriter

logger = logging.getLogger(__name__)


class BundleWriter(BundleWriterABC):
    """Writes a session bundle to disk.

    Args:
        sessions_dir: Root directory where all session bundles are stored.
                      Typically ``./sessions`` (configurable via settings).

    Example::

        writer = BundleWriter(sessions_dir=Path("./sessions"))
        writer.open_session("session_1714000000000_a3f9c2")
        writer.write_trace_event({"event": "session_start", "operator": "op-01"})
        writer.close_session()
    """

    def __init__(self, sessions_dir: Path) -> None:
        self._sessions_dir = sessions_dir
        self._session_id: str | None = None
        self._bundle_dir: Path | None = None
        self._trace: TraceWriter | None = None
        self._mcap: McapWriter | None = None

    @property
    def bundle_dir(self) -> Path | None:
        return self._bundle_dir

    def open_session(self, session_id: str, metadata: dict | None = None) -> None:
        """Initialise a new session bundle directory.

        Creates the directory and opens trace + MCAP writers.
        """
        self._session_id = session_id
        self._bundle_dir = self._sessions_dir / session_id
        self._bundle_dir.mkdir(parents=True, exist_ok=True)

        write_manifest(self._bundle_dir, session_id, metadata or {})

        self._trace = TraceWriter(self._bundle_dir)
        self._trace.open()

        self._mcap = McapWriter(self._bundle_dir)
        self._mcap.open()

        logger.info("[Bundle] Session opened: %s → %s", session_id, self._bundle_dir)

    def write_trace_event(self, event: dict) -> None:
        """Append a structured event to the NDJSON trace."""
        if self._trace is None:
            logger.warning("[Bundle] write_trace_event called before open_session — ignored")
            return
        self._trace.write(event)

    def close_session(self) -> None:
        """Finalise and flush the session bundle."""
        if self._trace:
            self._trace.close()
        if self._mcap:
            self._mcap.close()
        if self._bundle_dir:
            close_manifest(self._bundle_dir)
        logger.info("[Bundle] Session closed: %s", self._session_id)

        self._session_id = None
        self._bundle_dir = None
        self._trace = None
        self._mcap = None
