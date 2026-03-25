"""
third_arm.logging.replay_reader
─────────────────────────────────────────────────────────────────────────────
Session bundle replay reader.

Reads a bundle directory and yields events in chronological order.
Used by ``cli/replay_session.py`` and replay smoke tests.

TODO: add MCAP frame playback (Stage 1.5+).
TODO: add time-scaling for slow/fast replay.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator


class ReplayReader:
    """Reads a session bundle and yields events.

    Args:
        bundle_dir: Path to a session bundle directory.

    Example::

        reader = ReplayReader(Path("sessions/session_xyz"))
        reader.load()
        for event in reader.events():
            print(event)
    """

    def __init__(self, bundle_dir: Path) -> None:
        self._bundle_dir = bundle_dir
        self._manifest: dict = {}
        self._trace_lines: list[dict] = []

    def load(self) -> "ReplayReader":
        """Load bundle metadata and trace events into memory."""
        manifest_path = self._bundle_dir / "manifest.json"
        if manifest_path.exists():
            self._manifest = json.loads(manifest_path.read_text())

        trace_path = self._bundle_dir / "session_trace.ndjson"
        if trace_path.exists():
            self._trace_lines = [
                json.loads(line)
                for line in trace_path.read_text().splitlines()
                if line.strip()
            ]
        return self

    @property
    def manifest(self) -> dict:
        return self._manifest

    @property
    def session_id(self) -> str | None:
        return self._manifest.get("session_id")

    def events(self) -> Iterator[dict]:
        """Yield all trace events in file order.

        TODO: merge MCAP frames interleaved by timestamp (Stage 1.5+).
        """
        yield from self._trace_lines

    def summary(self) -> dict:
        """Return a brief summary of the bundle."""
        return {
            "session_id": self.session_id,
            "event_count": len(self._trace_lines),
            "created_at": self._manifest.get("created_at"),
            "closed_at": self._manifest.get("closed_at"),
        }
