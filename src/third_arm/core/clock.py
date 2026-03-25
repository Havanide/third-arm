"""
third_arm.core.clock
─────────────────────────────────────────────────────────────────────────────
Centralised time utilities.

Isolating time calls here makes replay and testing easier — stubs can
replace ``now_iso`` / ``now_ms`` without patching builtins everywhere.

TODO (Stage 1.5): support a monotonic hardware clock for MCAP timestamps.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone


def now_utc() -> datetime:
    """Return current UTC datetime (timezone-aware)."""
    return datetime.now(tz=timezone.utc)


def now_iso() -> str:
    """Return current UTC time as ISO-8601 string.

    Example: ``2024-04-25T10:30:00.123456+00:00``
    """
    return now_utc().isoformat()


def now_ms() -> int:
    """Return current Unix time in milliseconds (integer)."""
    return int(time.time() * 1000)


def now_ns() -> int:
    """Return current Unix time in nanoseconds.

    Used for MCAP log timestamps.
    """
    return time.time_ns()


# ── Process start reference ───────────────────────────────────────────────────
_START_NS: int = time.time_ns()


def uptime_s() -> float:
    """Return seconds elapsed since process start."""
    return (time.time_ns() - _START_NS) / 1e9
