"""
third_arm.adapters.vision.camera_stub
─────────────────────────────────────────────────────────────────────────────
Camera adapter stub — PLACEHOLDER for Stage 1.5.

Stage 1 is camera-ready but camera-off.
Enable by setting THIRD_ARM_CAMERA_ENABLED=true (requires physical camera).

TODO (Stage 1.5):
  - Implement OpenCV capture loop
  - Expose frame via async queue
  - Wire to ObservationStub → real object detector
"""

from __future__ import annotations

from third_arm.domain.contracts import CameraAdapterABC


class CameraStub(CameraAdapterABC):
    """No-op camera adapter for Stage 1.

    Returns blank/empty results so the rest of the stack can be tested
    without a physical camera attached.
    """

    async def capture_frame(self) -> bytes:
        """TODO: return a real JPEG frame from the connected camera."""
        return b""  # empty frame placeholder

    async def detect_objects(self) -> list[dict]:
        """TODO: run detection model and return bounding boxes + labels."""
        return []   # no detections in stub
