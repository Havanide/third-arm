"""
third_arm.adapters.vision.observation_stub
─────────────────────────────────────────────────────────────────────────────
Object observation pipeline stub — PLACEHOLDER for Stage 1.5.

TODO (Stage 1.5):
  - Wire camera frames to a detection model (YOLO / MobileNet-SSD)
  - Match detections against object catalogue (camera_class_label)
  - Publish Observation events to the event bus
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Observation:
    """A single detected object observation.

    TODO: add 3D position estimate from depth / stereo (Stage 2+).
    """

    class_label: str
    confidence: float
    bbox_xyxy: list[float] = field(default_factory=list)  # [x1, y1, x2, y2] pixels
    object_id: str | None = None                          # matched catalogue ID


class ObservationStub:
    """No-op observation pipeline for Stage 1.

    TODO: implement with real detection model for Stage 1.5.
    """

    async def get_observations(self) -> list[Observation]:
        """TODO: return current frame's detections."""
        return []
