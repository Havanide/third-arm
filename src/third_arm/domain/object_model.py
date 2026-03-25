"""
third_arm.domain.object_model
─────────────────────────────────────────────────────────────────────────────
Pydantic model for catalogue objects the arm can handle.
Mirrors the schema in configs/slots/stage1_objects.yaml.

TODO: add loader that reads the YAML catalogue at startup.
TODO (Stage 1.5): add camera_class_label matching logic.
"""

from __future__ import annotations

import functools
import logging
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field


class ObjectDimensions(BaseModel):
    """Physical bounding dimensions in millimetres."""

    diameter: float | None = None   # for cylindrical objects
    height: float | None = None
    width: float | None = None
    depth: float | None = None


class ArmObject(BaseModel):
    """A physical object the arm knows how to handle.

    Corresponds to an entry in ``stage1_objects.yaml``.
    """

    id: str = Field(..., description="Unique object identifier, e.g. 'obj_water_bottle_500ml'")
    label: str = Field(..., description="Human-readable display name")
    category: str = Field(..., description="Object category, e.g. 'drink', 'device'")
    default_slot: str = Field(..., description="Preferred slot_id when no slot is specified")
    grasp_type: str = Field(..., description="Grasp strategy: top_pinch | cylindrical_side | flat_side")
    mass_g: float = Field(0.0, description="Approximate mass in grams")
    dimensions_mm: ObjectDimensions = Field(default_factory=ObjectDimensions)
    camera_class_label: str | None = Field(
        None, description="COCO/custom class label for Stage 1.5 detector"
    )
    enabled: bool = True

    model_config = ConfigDict(frozen=True)  # objects are immutable catalogue entries


logger = logging.getLogger(__name__)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _default_catalog_path() -> Path:
    return _repo_root() / "configs" / "slots" / "stage1_objects.yaml"


@functools.lru_cache(maxsize=4)
def load_object_catalog(path: str | None = None) -> dict[str, ArmObject]:
    """Load object catalogue from YAML, with a small cached fallback.

    If the YAML file is missing, use the in-repo stub catalogue so the bootstrap
    flow remains runnable. Invalid YAML/schema still raises: bad config should
    fail loudly.
    """
    catalog_path = Path(path) if path else _default_catalog_path()
    if not catalog_path.exists():
        logger.warning("Object catalogue %s not found; falling back to stub catalogue", catalog_path)
        return {
            "obj_water_bottle_500ml": ArmObject(
                id="obj_water_bottle_500ml",
                label="Water bottle 500 ml",
                category="drink",
                default_slot="slot_A",
                grasp_type="cylindrical_side",
                mass_g=550,
                dimensions_mm=ObjectDimensions(diameter=65, height=200),
                camera_class_label="bottle",
            )
        }

    payload = yaml.safe_load(catalog_path.read_text(encoding="utf-8")) or {}
    items = payload.get("objects", [])
    return {item["id"]: ArmObject.model_validate(item) for item in items}


def clear_object_catalog_cache() -> None:
    load_object_catalog.cache_clear()


def get_object(object_id: str, path: str | None = None) -> ArmObject | None:
    """Look up an object by ID from YAML-backed catalogue."""
    return load_object_catalog(path).get(object_id)
