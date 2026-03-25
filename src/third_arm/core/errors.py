"""
third_arm.core.errors
─────────────────────────────────────────────────────────────────────────────
Domain exception hierarchy for the Third Arm service.

All custom exceptions inherit from ``ThirdArmError`` so callers can catch
the entire family with a single except clause.
"""

from __future__ import annotations


class ThirdArmError(Exception):
    """Base exception for all Third Arm service errors."""

    def __init__(self, message: str, code: str = "THIRD_ARM_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code!r}, message={self.message!r})"


# ── State machine errors ──────────────────────────────────────────────────────

class InvalidTransitionError(ThirdArmError):
    """Raised when a state transition is not allowed from the current state."""

    def __init__(self, from_state: str, trigger: str) -> None:
        super().__init__(
            f"Transition '{trigger}' is not valid from state '{from_state}'",
            code="INVALID_TRANSITION",
        )
        self.from_state = from_state
        self.trigger = trigger


class ArmNotReadyError(ThirdArmError):
    """Raised when a command is issued while the arm is not in ready state."""

    def __init__(self, current_state: str) -> None:
        super().__init__(
            f"Arm is not ready (current state: {current_state})",
            code="ARM_NOT_READY",
        )
        self.current_state = current_state


# ── Session errors ────────────────────────────────────────────────────────────

class SessionAlreadyActiveError(ThirdArmError):
    """Raised when a new session is requested while one is already active."""

    def __init__(self, session_id: str) -> None:
        super().__init__(
            f"Session '{session_id}' is already active",
            code="SESSION_ALREADY_ACTIVE",
        )


class NoActiveSessionError(ThirdArmError):
    """Raised when an operation requires an active session but none exists."""

    def __init__(self) -> None:
        super().__init__("No active session", code="NO_ACTIVE_SESSION")


# ── Hardware errors ───────────────────────────────────────────────────────────

class HardwareError(ThirdArmError):
    """Raised on hardware driver failure."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="HARDWARE_ERROR")


class EStopError(ThirdArmError):
    """Raised when emergency stop is triggered."""

    def __init__(self) -> None:
        super().__init__("Emergency stop activated", code="ESTOP")


# ── Config errors ─────────────────────────────────────────────────────────────

class ConfigError(ThirdArmError):
    """Raised on missing or invalid configuration."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="CONFIG_ERROR")
