"""
third_arm.domain.state_machine
─────────────────────────────────────────────────────────────────────────────
Arm state machine: agreed states and skeleton transition logic.

States (Stage 1 agreed set)
────────────────────────────
  boot            → initial power-on, firmware handshake (mock: instant)
  self_check      → running built-in diagnostics
  idle            → powered, no session, waiting for operator
  homing          → executing home trajectory
  ready           → at home, awaiting handover command
  task_arming     → loading task parameters, pre-grasp checks
  acquire         → moving to slot, grasping object
  lift            → raising object after grasp
  present         → at handover zone, presenting to operator
  transfer_wait   → holding, waiting for operator to take object
  release         → releasing gripper
  retract         → returning to home
  task_complete   → handover finished, logging closed
  task_aborted    → handover cancelled mid-task
  safe_stop       → controlled deceleration to standstill
  fault           → non-recoverable error, waiting for operator action
  recovering      → executing recovery procedure
  shutdown        → controlled power-down sequence

Trigger vocabulary (subset — extend as needed)
────────────────────────────────────────────────
  boot_complete, self_check_ok, self_check_fail,
  home_cmd, home_complete, home_fail,
  session_start, task_arm, acquire_cmd, lift_cmd,
  present_cmd, transfer_complete, release_cmd,
  retract_cmd, task_done, abort, estop,
  fault_clear, recover_ok, shutdown_cmd

TODO (Stage 1):  implement guard conditions and callbacks.
TODO (Stage 1.5): integrate real hardware timeouts.
TODO (Stage 2):   add intent-triggered transitions.
"""

from __future__ import annotations

from enum import Enum
from typing import Callable

from third_arm.core.clock import now_iso
from third_arm.core.errors import InvalidTransitionError


class ArmState(str, Enum):
    """Canonical arm state names."""

    BOOT = "boot"
    SELF_CHECK = "self_check"
    IDLE = "idle"
    HOMING = "homing"
    READY = "ready"
    TASK_ARMING = "task_arming"
    ACQUIRE = "acquire"
    LIFT = "lift"
    PRESENT = "present"
    TRANSFER_WAIT = "transfer_wait"
    RELEASE = "release"
    RETRACT = "retract"
    TASK_COMPLETE = "task_complete"
    TASK_ABORTED = "task_aborted"
    SAFE_STOP = "safe_stop"
    FAULT = "fault"
    RECOVERING = "recovering"
    SHUTDOWN = "shutdown"


# ── Allowed transitions ────────────────────────────────────────────────────────
# Format: { ArmState → { trigger → ArmState } }
# Only explicitly listed transitions are permitted.
TRANSITIONS: dict[ArmState, dict[str, ArmState]] = {
    ArmState.BOOT: {
        "boot_complete":   ArmState.SELF_CHECK,
        "shutdown_cmd":    ArmState.SHUTDOWN,
    },
    ArmState.SELF_CHECK: {
        "self_check_ok":   ArmState.IDLE,
        "self_check_fail": ArmState.FAULT,
        "shutdown_cmd":    ArmState.SHUTDOWN,
    },
    ArmState.IDLE: {
        "home_cmd":        ArmState.HOMING,
        "shutdown_cmd":    ArmState.SHUTDOWN,
        "estop":           ArmState.SAFE_STOP,
    },
    ArmState.HOMING: {
        "home_complete":   ArmState.READY,
        "home_fail":       ArmState.FAULT,
        "estop":           ArmState.SAFE_STOP,
        "abort":           ArmState.SAFE_STOP,
    },
    ArmState.READY: {
        "session_start":   ArmState.TASK_ARMING,
        "home_cmd":        ArmState.HOMING,
        "shutdown_cmd":    ArmState.SHUTDOWN,
        "estop":           ArmState.SAFE_STOP,
    },
    ArmState.TASK_ARMING: {
        "task_arm":        ArmState.ACQUIRE,
        "abort":           ArmState.TASK_ABORTED,
        "estop":           ArmState.SAFE_STOP,
    },
    ArmState.ACQUIRE: {
        "lift_cmd":        ArmState.LIFT,
        "abort":           ArmState.TASK_ABORTED,
        "estop":           ArmState.SAFE_STOP,
    },
    ArmState.LIFT: {
        "present_cmd":     ArmState.PRESENT,
        "abort":           ArmState.TASK_ABORTED,
        "estop":           ArmState.SAFE_STOP,
    },
    ArmState.PRESENT: {
        "transfer_complete": ArmState.TRANSFER_WAIT,
        "abort":           ArmState.TASK_ABORTED,
        "estop":           ArmState.SAFE_STOP,
    },
    ArmState.TRANSFER_WAIT: {
        "release_cmd":     ArmState.RELEASE,
        "abort":           ArmState.TASK_ABORTED,
        "estop":           ArmState.SAFE_STOP,
    },
    ArmState.RELEASE: {
        "retract_cmd":     ArmState.RETRACT,
        "estop":           ArmState.SAFE_STOP,
    },
    ArmState.RETRACT: {
        "task_done":       ArmState.TASK_COMPLETE,
        "estop":           ArmState.SAFE_STOP,
    },
    ArmState.TASK_COMPLETE: {
        "home_cmd":        ArmState.HOMING,
        "shutdown_cmd":    ArmState.SHUTDOWN,
    },
    ArmState.TASK_ABORTED: {
        "home_cmd":        ArmState.HOMING,
        "estop":           ArmState.SAFE_STOP,
        "shutdown_cmd":    ArmState.SHUTDOWN,
    },
    ArmState.SAFE_STOP: {
        "home_cmd":        ArmState.HOMING,
        "fault_clear":     ArmState.IDLE,
        "shutdown_cmd":    ArmState.SHUTDOWN,
    },
    ArmState.FAULT: {
        "fault_clear":     ArmState.RECOVERING,
        "shutdown_cmd":    ArmState.SHUTDOWN,
    },
    ArmState.RECOVERING: {
        "recover_ok":      ArmState.IDLE,
        "estop":           ArmState.SAFE_STOP,
        "self_check_fail": ArmState.FAULT,
    },
    ArmState.SHUTDOWN: {
        # Terminal state — no outgoing transitions
    },
}


class StateMachine:
    """Lightweight arm state machine.

    Args:
        initial: Starting state (default: BOOT).
        on_transition: Optional callback invoked after every successful transition.
            Signature: ``callback(from_state, trigger, to_state, ts_iso) -> None``.

    Example::

        sm = StateMachine()
        sm.trigger("boot_complete")   # BOOT → SELF_CHECK
        sm.trigger("self_check_ok")   # SELF_CHECK → IDLE
    """

    def __init__(
        self,
        initial: ArmState = ArmState.BOOT,
        on_transition: Callable[[ArmState, str, ArmState, str], None] | None = None,
    ) -> None:
        self._state = initial
        self._on_transition = on_transition
        self.history: list[dict] = []  # lightweight audit log

    @property
    def state(self) -> ArmState:
        return self._state

    def can_trigger(self, trigger: str) -> bool:
        """Return True if *trigger* is valid from the current state."""
        return trigger in TRANSITIONS.get(self._state, {})

    def trigger(self, trigger_name: str) -> ArmState:
        """Apply *trigger_name* and transition to the next state.

        Raises:
            InvalidTransitionError: if the trigger is not valid in the current state.
        """
        allowed = TRANSITIONS.get(self._state, {})
        if trigger_name not in allowed:
            raise InvalidTransitionError(self._state.value, trigger_name)

        from_state = self._state
        to_state = allowed[trigger_name]
        ts = now_iso()

        self._state = to_state
        record = {
            "ts": ts,
            "from": from_state.value,
            "trigger": trigger_name,
            "to": to_state.value,
        }
        self.history.append(record)

        if self._on_transition:
            self._on_transition(from_state, trigger_name, to_state, ts)

        return to_state

    def __repr__(self) -> str:
        return f"StateMachine(state={self._state.value!r})"
