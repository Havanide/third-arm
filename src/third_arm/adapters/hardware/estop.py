"""
third_arm.adapters.hardware.estop
─────────────────────────────────────────────────────────────────────────────
Emergency stop handler — STUB / PLACEHOLDER.

The e-stop is a hardware-level safety interlock and MUST be wired before
any Stage 1.5 physical hardware testing.

NOTE: The server is NOT in the safety-critical loop.  The physical e-stop
circuit must interrupt motor power independently of software.  This adapter
only provides the *software notification* that an e-stop occurred.

TODO (Stage 1.5):
  - Wire GPIO e-stop sense line
  - Trigger state machine estop event
  - Notify all connected WebSocket clients
  - Log EStopEvent to bundle
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class EStopMonitor:
    """Monitors the hardware e-stop line and raises software alerts.

    TODO: implement for Stage 1.5.
    """

    def __init__(self, pin: int) -> None:
        self._pin = pin
        logger.warning("[EStop] EStopMonitor not implemented — hardware estop not monitored")

    def start(self) -> None:
        """TODO: begin monitoring e-stop GPIO line."""

    def stop(self) -> None:
        """TODO: stop monitoring."""

    def is_active(self) -> bool:
        """TODO: return True if e-stop is currently pressed."""
        return False  # optimistic stub
