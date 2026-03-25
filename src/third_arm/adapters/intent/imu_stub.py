"""
third_arm.adapters.intent.imu_stub
─────────────────────────────────────────────────────────────────────────────
IMU (Inertial Measurement Unit) adapter stub — PLACEHOLDER for Stage 2.

TODO (Stage 2):
  - Choose IMU hardware (e.g. BNO085, MPU-6050)
  - Implement serial/I²C read loop
  - Publish IMU readings to intent classifier
"""

from __future__ import annotations

from third_arm.domain.contracts import IntentAdapterABC


class ImuStub(IntentAdapterABC):
    """No-op IMU stub returning zeroed readings."""

    async def get_imu_reading(self) -> dict:
        """TODO: return real IMU sample from hardware."""
        return {
            "accel": {"x": 0.0, "y": 0.0, "z": 9.81},
            "gyro":  {"x": 0.0, "y": 0.0, "z": 0.0},
            "orientation": {"roll": 0.0, "pitch": 0.0, "yaw": 0.0},
            "mock": True,
        }

    async def get_semg_reading(self) -> dict:
        """Not applicable to IMU — delegated to SemgStub."""
        return {}
