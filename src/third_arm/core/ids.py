"""
third_arm.core.ids
─────────────────────────────────────────────────────────────────────────────
Deterministic, human-readable ID generation utilities.

All IDs in the system follow the pattern:
    <prefix>_<timestamp_ms>_<random_suffix>

This makes logs grepping-friendly without requiring a database.
"""

from __future__ import annotations

import time
import uuid


def _suffix(n: int = 6) -> str:
    """Return first *n* hex chars of a random UUID4."""
    return uuid.uuid4().hex[:n]


def new_session_id() -> str:
    """Generate a unique session bundle ID.

    Example: ``session_1714000000000_a3f9c2``
    """
    ts = int(time.time() * 1000)
    return f"session_{ts}_{_suffix()}"


def new_handover_id() -> str:
    """Generate a unique handover event ID.

    Example: ``hov_1714000000000_b1e4d7``
    """
    ts = int(time.time() * 1000)
    return f"hov_{ts}_{_suffix()}"


def new_trace_id() -> str:
    """Generate a lightweight trace ID for request correlation."""
    return f"trace_{_suffix(8)}"
