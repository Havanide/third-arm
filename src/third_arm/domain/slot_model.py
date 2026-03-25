"""
third_arm.domain.slot_model
─────────────────────────────────────────────────────────────────────────────
Pydantic model for physical storage slots the arm can reach.
Mirrors the schema in configs/slots/stage1_slots.yaml.

TODO: add YAML loader.
TODO (Stage 1.5): add slot occupancy tracking (from camera detections).
"""

from __future__ import annotations

import functools
import logging
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field


class Position3D(BaseModel):
    """Cartesian position in arm-local frame (millimetres)."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


class Slot(BaseModel):
    """A physical storage slot in the arm's workspace."""

    id: str = Field(..., description="Unique slot identifier, e.g. 'slot_A'")
    label: str = Field(..., description="Human-readable display name")
    enabled: bool = True
    position: Position3D = Field(default_factory=Position3D)
    approach_angle_deg: float = 0.0
    grasp_type: str = "top_pinch"
    notes: str = ""

    model_config = ConfigDict(frozen=True)


class HandoverZone(BaseModel):
    """The zone where the arm presents objects to the operator."""

    label: str = "Operator handover point"
    position: Position3D = Field(default_factory=Position3D)
    clearance_radius_mm: float = 80.0


logger = logging.getLogger(__name__)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _default_slot_path() -> Path:
    return _repo_root() / "configs" / "slots" / "stage1_slots.yaml"


@functools.lru_cache(maxsize=4)
def load_slot_catalog(path: str | None = None) -> dict[str, Slot]:
    """Load slot catalogue from YAML, with cached stub fallback."""
    slot_path = Path(path) if path else _default_slot_path()
    if not slot_path.exists():
        logger.warning("Slot catalogue %s not found; falling back to stub slots", slot_path)
        return {
            "slot_A": Slot(
                id="slot_A",
                label="Slot A — left tray",
                enabled=True,
                position=Position3D(x=150, y=50, z=120),
                approach_angle_deg=45,
            ),
            "slot_B": Slot(
                id="slot_B",
                label="Slot B — centre tray",
                enabled=True,
                position=Position3D(x=150, y=0, z=120),
                approach_angle_deg=0,
            ),
        }

    payload = yaml.safe_load(slot_path.read_text(encoding="utf-8")) or {}
    items = payload.get("slots", [])
    return {item["id"]: Slot.model_validate(item) for item in items}


@functools.lru_cache(maxsize=4)
def load_handover_zone(path: str | None = None) -> HandoverZone:
    slot_path = Path(path) if path else _default_slot_path()
    if not slot_path.exists():
        logger.warning("Slot catalogue %s not found; using default handover zone", slot_path)
        return HandoverZone()

    payload = yaml.safe_load(slot_path.read_text(encoding="utf-8")) or {}
    zone = payload.get("handover_zone", {})
    return HandoverZone.model_validate(zone) if zone else HandoverZone()


def clear_slot_catalog_cache() -> None:
    load_slot_catalog.cache_clear()
    load_handover_zone.cache_clear()


def get_slot(slot_id: str, path: str | None = None) -> Slot | None:
    """Look up a slot by ID from YAML-backed catalogue."""
    return load_slot_catalog(path).get(slot_id)
