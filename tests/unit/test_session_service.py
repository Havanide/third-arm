from __future__ import annotations

from pathlib import Path

import pytest

from third_arm.domain.session_service import SessionService


class _StartRollbackBundleWriter:
    def __init__(self) -> None:
        self.bundle_dir: Path | None = None
        self.close_calls = 0
        self.fail_session_started_once = True

    def open_session(self, session_id, metadata=None) -> None:
        self.bundle_dir = Path("/tmp") / session_id

    def write_trace_event(self, event) -> None:
        if event["event"] == "session_started" and self.fail_session_started_once:
            self.fail_session_started_once = False
            raise RuntimeError("trace write failed")

    def close_session(self) -> None:
        self.close_calls += 1


class _StopRetryBundleWriter:
    def __init__(self) -> None:
        self.bundle_dir: Path | None = None
        self.close_calls = 0
        self.events: list[dict] = []

    def open_session(self, session_id, metadata=None) -> None:
        self.bundle_dir = Path("/tmp") / session_id

    def write_trace_event(self, event) -> None:
        self.events.append(dict(event))

    def close_session(self) -> None:
        self.close_calls += 1
        if self.close_calls == 1:
            raise RuntimeError("close failed")


def test_start_rolls_back_when_initial_trace_write_fails():
    writer = _StartRollbackBundleWriter()
    svc = SessionService(bundle_writer=writer)

    with pytest.raises(RuntimeError, match="trace write failed"):
        svc.start(operator_id="test-op")

    assert svc.active is None
    assert writer.close_calls == 1

    session = svc.start(operator_id="test-op")
    assert svc.active is session


def test_stop_keeps_active_session_until_bundle_close_succeeds():
    writer = _StopRetryBundleWriter()
    svc = SessionService(bundle_writer=writer)
    session = svc.start(operator_id="test-op")

    with pytest.raises(RuntimeError, match="close failed"):
        svc.stop()

    assert svc.active is session
    assert svc.active.stopped_at is None
    assert [event["event"] for event in writer.events].count("session_stopped") == 1

    stopped = svc.stop()
    assert stopped.session_id == session.session_id
    assert stopped.stopped_at is not None
    assert svc.active is None
    assert [event["event"] for event in writer.events].count("session_stopped") == 1
