"""
tests/unit/test_imports.py
─────────────────────────────────────────────────────────────────────────────
Smoke tests: verify that all public modules import without errors.

This is the minimal bar — if these fail the project structure is broken.
"""

import pytest


def test_core_imports():
    from third_arm.core import settings, ids, clock, errors  # noqa: F401


def test_domain_imports():
    from third_arm.domain import (  # noqa: F401
        state_machine,
        contracts,
        object_model,
        slot_model,
        policies,
        session_service,
        handover_service,
    )


def test_api_imports():
    from third_arm.api import deps  # noqa: F401
    from third_arm.api.routers import health, status, session, arm, handover, artifacts  # noqa: F401
    from third_arm.api.ws import stream  # noqa: F401
    from third_arm.api.schemas import common, commands, events, telemetry, faults  # noqa: F401


def test_adapters_imports():
    from third_arm.adapters.mock_arm import driver  # noqa: F401
    from third_arm.adapters.hardware import arm_driver, estop, power_monitor  # noqa: F401
    from third_arm.adapters.vision import camera_stub, observation_stub  # noqa: F401
    from third_arm.adapters.intent import imu_stub, semg_stub  # noqa: F401


def test_logging_imports():
    from third_arm.logging import (  # noqa: F401
        bundle_writer,
        trace_writer,
        mcap_writer,
        manifest,
        replay_reader,
    )


def test_storage_imports():
    from third_arm.storage import paths, files  # noqa: F401


def test_cli_imports():
    from third_arm.cli import run_dev, export_bundle, replay_session  # noqa: F401


def test_state_machine_initial_state():
    from third_arm.domain.state_machine import ArmState, StateMachine
    sm = StateMachine()
    assert sm.state == ArmState.BOOT


def test_state_machine_transitions():
    from third_arm.domain.state_machine import ArmState, StateMachine
    sm = StateMachine()
    sm.trigger("boot_complete")
    assert sm.state == ArmState.SELF_CHECK
    sm.trigger("self_check_ok")
    assert sm.state == ArmState.IDLE


def test_state_machine_invalid_transition():
    from third_arm.core.errors import InvalidTransitionError
    from third_arm.domain.state_machine import StateMachine
    sm = StateMachine()
    with pytest.raises(InvalidTransitionError):
        sm.trigger("nonexistent_trigger")


def test_ids_are_unique():
    from third_arm.core.ids import new_session_id
    ids = {new_session_id() for _ in range(100)}
    assert len(ids) == 100


class _NullBundleWriter:
    """Minimal stub for unit tests — discards all calls."""

    bundle_dir = None

    def open_session(self, session_id, metadata=None):
        pass

    def write_trace_event(self, event):
        pass

    def close_session(self):
        pass


def test_session_service_start_stop():
    from third_arm.domain.session_service import SessionService
    svc = SessionService(bundle_writer=_NullBundleWriter())
    session = svc.start(operator_id="test-op")
    assert session.is_active
    stopped = svc.stop()
    assert not stopped.is_active


def test_session_service_double_start_raises():
    from third_arm.core.errors import SessionAlreadyActiveError
    from third_arm.domain.session_service import SessionService
    svc = SessionService(bundle_writer=_NullBundleWriter())
    svc.start()
    with pytest.raises(SessionAlreadyActiveError):
        svc.start()
