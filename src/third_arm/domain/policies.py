"""
third_arm.domain.policies
─────────────────────────────────────────────────────────────────────────────
Business rule / policy functions.

Policies validate inputs or preconditions *before* commands are executed.
They are pure functions with no side effects.

TODO: expand with real safety policies (weight limits, workspace bounds, etc.)
"""

from __future__ import annotations

from third_arm.domain.object_model import ArmObject
from third_arm.domain.slot_model import Slot


def can_grasp(obj: ArmObject, slot: Slot) -> tuple[bool, str]:
    """Return (allowed, reason) for a proposed grasp.

    Args:
        obj:  The object to grasp.
        slot: The slot to grasp from.

    Returns:
        ``(True, "ok")`` if the grasp is allowed, or
        ``(False, "<reason>")`` otherwise.

    TODO: add real guard conditions:
      - workspace reachability check
      - weight / payload limit
      - slot occupancy (Stage 1.5 vision)
      - e-stop state
    """
    if not obj.enabled:
        return False, f"Object '{obj.id}' is disabled in catalogue"
    if not slot.enabled:
        return False, f"Slot '{slot.id}' is disabled"
    # TODO: check grasp_type compatibility between object and slot
    return True, "ok"


def can_start_session(current_session_id: str | None) -> tuple[bool, str]:
    """Return (allowed, reason) for starting a new session.

    TODO: add operator authentication check (Stage 2+).
    """
    if current_session_id is not None:
        return False, f"Session '{current_session_id}' is already active"
    return True, "ok"
