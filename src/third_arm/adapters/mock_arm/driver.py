"""
third_arm.adapters.mock_arm.driver
─────────────────────────────────────────────────────────────────────────────
Mock arm driver — simulates hardware responses without physical hardware.

Used in Stage 1 (desktop-first) and in all automated tests.

All methods log their calls and sleep briefly to simulate latency.
Replace this with the real hardware driver (adapters/hardware/arm_driver.py)
by toggling THIRD_ARM_MOCK_HARDWARE=false and implementing ArmDriverABC.
"""

from __future__ import annotations

import asyncio
import logging

from third_arm.domain.contracts import ArmDriverABC

logger = logging.getLogger(__name__)

# Simulated motion latencies (seconds)
_HOME_LATENCY    = 0.3
_HANDOVER_LATENCY = 0.5
_STOP_LATENCY    = 0.1


class MockArmDriver(ArmDriverABC):
    """Simulated arm driver for Stage 1 / testing.

    Maintains a fake joint state so telemetry looks plausible.
    """

    def __init__(self) -> None:
        self._joint_angles: list[float] = [0.0, -30.0, 90.0, 0.0, 0.0, 0.0]
        self._gripper_pct: float = 0.0
        self._ee_position: dict = {"x": 0.0, "y": 0.0, "z": 150.0}
        logger.info("[MockArm] Initialised")

    async def home(self) -> None:
        """Simulate homing motion."""
        logger.info("[MockArm] home() called — simulating %ss motion", _HOME_LATENCY)
        await asyncio.sleep(_HOME_LATENCY)
        self._joint_angles = [0.0, -30.0, 90.0, 0.0, 0.0, 0.0]
        self._gripper_pct = 0.0
        self._ee_position = {"x": 0.0, "y": 0.0, "z": 150.0}
        logger.info("[MockArm] home() complete")

    async def start_handover(self, slot_id: str, object_id: str) -> None:
        """Simulate a full pick-and-present sequence."""
        logger.info("[MockArm] start_handover(slot=%s, object=%s)", slot_id, object_id)
        await asyncio.sleep(_HANDOVER_LATENCY)
        # Fake: move towards slot
        self._joint_angles = [10.0, -45.0, 80.0, 5.0, -10.0, 0.0]
        self._gripper_pct = 80.0
        self._ee_position = {"x": 150.0, "y": 50.0, "z": 120.0}
        logger.info("[MockArm] start_handover() complete")

    async def safe_stop(self) -> None:
        """Simulate emergency deceleration."""
        logger.warning("[MockArm] safe_stop() called — simulating stop")
        await asyncio.sleep(_STOP_LATENCY)
        logger.warning("[MockArm] safe_stop() complete — arm halted")

    async def get_telemetry(self) -> dict:
        """Return current fake telemetry snapshot."""
        return {
            "joint_angles_deg": list(self._joint_angles),
            "ee_position_mm": dict(self._ee_position),
            "gripper_pct": self._gripper_pct,
            "mock": True,
        }
