"""
third_arm.domain.contracts
─────────────────────────────────────────────────────────────────────────────
Abstract base classes (contracts / ports) that define the interfaces adapters
must implement.  The domain layer depends only on these ABCs — never on
concrete adapter implementations.

This is the Ports & Adapters (Hexagonal Architecture) boundary.

TODO: add abstract methods as concrete adapter capabilities are defined.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ArmDriverABC(ABC):
    """Port: physical (or simulated) arm control."""

    @abstractmethod
    async def home(self) -> None:
        """Move arm to home / safe position."""
        ...

    @abstractmethod
    async def start_handover(self, slot_id: str, object_id: str) -> None:
        """Execute the handover sequence for the given slot/object."""
        ...

    @abstractmethod
    async def safe_stop(self) -> None:
        """Immediately decelerate and hold."""
        ...

    @abstractmethod
    async def get_telemetry(self) -> dict:
        """Return a snapshot of current joint angles, EE position, gripper state."""
        ...


class CameraAdapterABC(ABC):
    """Port: camera / vision pipeline.  Stage 1.5+."""

    @abstractmethod
    async def capture_frame(self) -> bytes:
        """Return a JPEG-encoded frame as bytes."""
        ...

    @abstractmethod
    async def detect_objects(self) -> list[dict]:
        """Return a list of detected objects with bounding boxes and class labels."""
        ...


class IntentAdapterABC(ABC):
    """Port: IMU / sEMG intent sensing.  Stage 2+."""

    @abstractmethod
    async def get_imu_reading(self) -> dict:
        """Return latest IMU sample (accel, gyro, orientation)."""
        ...

    @abstractmethod
    async def get_semg_reading(self) -> dict:
        """Return latest sEMG sample (channel values, gesture class)."""
        ...


class BundleWriterABC(ABC):
    """Port: session bundle / replay logging."""

    @abstractmethod
    def open_session(self, session_id: str) -> None:
        """Initialise a new session bundle directory."""
        ...

    @abstractmethod
    def write_trace_event(self, event: dict) -> None:
        """Append a structured event to the session trace."""
        ...

    @abstractmethod
    def close_session(self) -> None:
        """Finalise and flush the session bundle."""
        ...
