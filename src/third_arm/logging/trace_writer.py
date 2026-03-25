"""
third_arm.logging.trace_writer
─────────────────────────────────────────────────────────────────────────────
Newline-delimited JSON (NDJSON) trace writer.

Each session writes a ``session_trace.ndjson`` file where every line is
a JSON object representing a discrete event (state transition, command,
handover step, fault, etc.).

This file is human-readable and grep-friendly — designed for post-hoc
debugging without needing a replay tool.

TODO: add async file I/O (aiofiles) to avoid blocking the event loop.
TODO: add log rotation / size cap for long-running sessions.
"""

from __future__ import annotations

import json
from pathlib import Path

from third_arm.core.clock import now_iso


class TraceWriter:
    """Appends structured events to an NDJSON trace file.

    Args:
        bundle_dir: Session bundle directory where the trace file lives.

    Example::

        writer = TraceWriter(bundle_dir=Path("sessions/session_xyz"))
        writer.open()
        writer.write({"event": "arm_homed", "ts": now_iso()})
        writer.close()
    """

    FILENAME = "session_trace.ndjson"

    def __init__(self, bundle_dir: Path) -> None:
        self._path = bundle_dir / self.FILENAME
        self._fh = None

    def open(self) -> None:
        """Open (or create) the trace file for appending."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self._path.open("a", encoding="utf-8")

    def write(self, event: dict) -> None:
        """Append a single event as a JSON line.

        A ``ts`` key is injected if not already present.
        """
        if self._fh is None:
            raise RuntimeError("TraceWriter is not open — call open() first")
        event.setdefault("ts", now_iso())
        self._fh.write(json.dumps(event, default=str) + "\n")
        self._fh.flush()  # TODO: batch-flush on interval for performance

    def close(self) -> None:
        """Flush and close the trace file."""
        if self._fh:
            self._fh.flush()
            self._fh.close()
            self._fh = None
