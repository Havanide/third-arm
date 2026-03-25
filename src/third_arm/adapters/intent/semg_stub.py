"""
third_arm.adapters.intent.semg_stub
─────────────────────────────────────────────────────────────────────────────
sEMG (surface electromyography) adapter stub — PLACEHOLDER for Stage 2.

TODO (Stage 2):
  - Choose sEMG hardware (e.g. Myo armband, custom ADS1299 board)
  - Implement sample acquisition loop
  - Apply pre-processing (bandpass filter, RMS envelope)
  - Feed into gesture classifier
"""

from __future__ import annotations

from third_arm.domain.contracts import IntentAdapterABC


class SemgStub(IntentAdapterABC):
    """No-op sEMG stub returning zero readings."""

    async def get_imu_reading(self) -> dict:
        """Not applicable to sEMG — delegated to ImuStub."""
        return {}

    async def get_semg_reading(self) -> dict:
        """TODO: return real sEMG sample from hardware."""
        return {
            "channels": [0.0] * 8,   # 8-channel stub
            "gesture_class": None,
            "confidence": 0.0,
            "mock": True,
        }
