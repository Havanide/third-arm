"""
third_arm.logging.mcap_writer
─────────────────────────────────────────────────────────────────────────────
MCAP telemetry writer — placeholder for Stage 1.

MCAP (https://mcap.dev) is a binary container format for robotics logs,
compatible with Foxglove Studio for replay and visualisation.

Stage 1: creates an empty / placeholder ``telemetry.mcap`` file so the
bundle structure is correct.  Real binary telemetry writing is deferred
to Stage 1.5 when hardware streams are available.

TODO (Stage 1.5):
  - Define MCAP schemas for TelemetryFrame, StateTransition, Fault
  - Open MCAP writer in lifespan and stream records per-frame
  - Close and finalise on session end
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class McapWriter:
    """Placeholder MCAP writer.

    Creates the target file at open() and writes a minimal header comment.
    Replace the body with real mcap library calls in Stage 1.5.

    TODO: use ``mcap.writer.Writer`` from the mcap package.
    """

    FILENAME = "telemetry.mcap"

    def __init__(self, bundle_dir: Path) -> None:
        self._path = bundle_dir / self.FILENAME
        self._opened = False

    def open(self) -> None:
        """Create the MCAP file placeholder."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        # TODO: replace with real MCAP writer initialisation
        # For now, create an empty file so the bundle manifest can reference it
        self._path.touch()
        self._opened = True
        logger.info("[McapWriter] Placeholder MCAP file created: %s", self._path)

    def write_telemetry(self, frame: dict) -> None:
        """TODO: serialise TelemetryFrame and write an MCAP record."""
        if not self._opened:
            raise RuntimeError("McapWriter is not open — call open() first")
        # TODO: encode frame as JSON or protobuf schema and write to MCAP
        logger.debug("[McapWriter] STUB write_telemetry called (not written to file)")

    def close(self) -> None:
        """TODO: finalise MCAP file (write footer, CRC)."""
        if self._opened:
            logger.info("[McapWriter] Placeholder MCAP closed: %s", self._path)
            self._opened = False
