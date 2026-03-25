"""
tests/replay/test_bundle_smoke.py
─────────────────────────────────────────────────────────────────────────────
Smoke tests for bundle writer and replay reader.
"""

import json
from pathlib import Path

import pytest


@pytest.fixture
def tmp_sessions(tmp_path):
    return tmp_path / "sessions"


def test_bundle_writer_creates_files(tmp_sessions):
    from third_arm.logging.bundle_writer import BundleWriter

    writer = BundleWriter(tmp_sessions)
    writer.open_session("test_session_001", metadata={"operator": "test"})
    writer.write_trace_event({"event": "test_event", "value": 42})
    writer.close_session()

    bundle_dir = tmp_sessions / "test_session_001"
    assert bundle_dir.exists()
    assert (bundle_dir / "manifest.json").exists()
    assert (bundle_dir / "session_trace.ndjson").exists()
    assert (bundle_dir / "telemetry.mcap").exists()


def test_manifest_contains_session_id(tmp_sessions):
    from third_arm.logging.bundle_writer import BundleWriter

    writer = BundleWriter(tmp_sessions)
    writer.open_session("test_session_002")
    writer.close_session()

    manifest = json.loads((tmp_sessions / "test_session_002" / "manifest.json").read_text())
    assert manifest["session_id"] == "test_session_002"
    assert manifest["closed_at"] is not None


def test_replay_reader_reads_events(tmp_sessions):
    from third_arm.logging.bundle_writer import BundleWriter
    from third_arm.logging.replay_reader import ReplayReader

    writer = BundleWriter(tmp_sessions)
    writer.open_session("test_session_003")
    writer.write_trace_event({"event": "e1"})
    writer.write_trace_event({"event": "e2"})
    writer.close_session()

    reader = ReplayReader(tmp_sessions / "test_session_003").load()
    events = list(reader.events())
    assert len(events) == 2
    assert events[0]["event"] == "e1"
    assert events[1]["event"] == "e2"


def test_list_session_bundles(tmp_sessions):
    from third_arm.logging.bundle_writer import BundleWriter
    from third_arm.storage.paths import list_session_bundles

    for i in range(3):
        writer = BundleWriter(tmp_sessions)
        writer.open_session(f"test_session_{i:03d}")
        writer.close_session()

    bundles = list_session_bundles(tmp_sessions)
    assert len(bundles) == 3
