"""
tests/integration/test_full_flow.py
─────────────────────────────────────────────────────────────────────────────
E2E integration test: full Stage 1 operator flow through HTTP.

Flow:
  app startup
  → POST /arm/home          (IDLE → HOMING → READY)
  → POST /session/start     (opens bundle, emits session_started)
  → POST /handover/request  (executes mock sequence, emits handover events)
  → POST /session/stop      (emits session_stopped, closes bundle)
  → GET  /artifacts         (bundle visible in listing)

Assertions verify:
  - All HTTP status codes
  - Bundle files exist on disk: manifest.json, session_trace.ndjson, telemetry.mcap
  - manifest["closed_at"] is set after stop
  - Trace contains "session_started" and "handover_completed" events
"""

from __future__ import annotations

import json

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from third_arm.core.settings import get_settings
from third_arm.logging.replay_reader import ReplayReader
from third_arm.main import create_app


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest_asyncio.fixture
async def client(tmp_path, monkeypatch):
    """AsyncClient with isolated sessions directory wired into settings."""
    monkeypatch.setenv("THIRD_ARM_SESSIONS_DIR", str(tmp_path))
    get_settings.cache_clear()
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        async with app.router.lifespan_context(app):
            yield ac


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_full_session_handover_flow(client, tmp_path):
    """Full operator flow produces a valid, closed session bundle on disk."""

    # ── 1. Home the arm: IDLE → READY ────────────────────────────────────────
    resp = await client.post("/arm/home")
    assert resp.status_code == 202, resp.text
    assert resp.json()["new_state"] == "ready"

    # ── 2. Start a session ────────────────────────────────────────────────────
    resp = await client.post(
        "/session/start",
        json={
            "operator_id": "test_op",
            "object_id": "obj_water_bottle_500ml",
            "slot_id": "slot_A",
            "notes": "integration test run",
        },
    )
    assert resp.status_code == 200, resp.text
    start_data = resp.json()
    session_id = start_data["session_id"]

    assert session_id.startswith("session_")
    assert set(start_data) == {"session_id", "started_at", "operator_id"}
    bundle_dir = tmp_path / session_id

    # ── 3. Request a handover ─────────────────────────────────────────────────
    resp = await client.post(
        "/handover/request",
        json={"object_id": "obj_water_bottle_500ml", "slot_id": "slot_A"},
    )
    assert resp.status_code == 202, resp.text
    handover_data = resp.json()
    assert handover_data["status"] == "complete"
    handover_id = handover_data["handover_id"]
    assert handover_id.startswith("hov_")
    assert set(handover_data) == {"handover_id", "object_id", "slot_id", "completed_at", "status"}

    # ── 4. Stop the session ───────────────────────────────────────────────────
    resp = await client.post("/session/stop")
    assert resp.status_code == 200, resp.text
    stop_data = resp.json()
    assert stop_data["session_id"] == session_id
    assert stop_data["status"] == "stopped"

    # ── 5. Verify bundle files exist on disk ──────────────────────────────────
    assert bundle_dir.exists(), f"Bundle directory not found: {bundle_dir}"
    assert (bundle_dir / "manifest.json").exists(), "manifest.json missing"
    assert (bundle_dir / "session_trace.ndjson").exists(), "session_trace.ndjson missing"
    assert (bundle_dir / "telemetry.mcap").exists(), "telemetry.mcap missing"

    # ── 6. Verify manifest is closed ─────────────────────────────────────────
    manifest = json.loads((bundle_dir / "manifest.json").read_text())
    assert manifest["session_id"] == session_id
    assert manifest["closed_at"] is not None, "manifest.closed_at should be set after stop"

    # ── 7. Verify trace event contents ───────────────────────────────────────
    reader = ReplayReader(bundle_dir).load()
    events = list(reader.events())
    event_names = [e["event"] for e in events]

    assert "session_started" in event_names, f"session_started missing; events: {event_names}"
    assert "handover_requested" in event_names, f"handover_requested missing"
    assert "handover_driver_started" in event_names, f"handover_driver_started missing"
    assert "handover_completed" in event_names, f"handover_completed missing"
    assert "session_stopped" in event_names, f"session_stopped missing"

    # Verify ordering: session_started comes first, session_stopped comes last
    assert event_names[0] == "session_started"
    assert event_names[-1] == "session_stopped"

    # ── 8. Verify GET /artifacts sees the bundle ──────────────────────────────
    resp = await client.get("/artifacts")
    assert resp.status_code == 200, resp.text
    artifacts_data = resp.json()
    bundle_ids = [b["session_id"] for b in artifacts_data["bundles"]]
    assert session_id in bundle_ids, f"Session {session_id} not in artifacts: {bundle_ids}"


@pytest.mark.asyncio
async def test_handover_requires_active_session(client):
    """POST /handover/request should reject requests when no session is active."""

    resp = await client.post("/arm/home")
    assert resp.status_code == 202, resp.text

    resp = await client.post(
        "/handover/request",
        json={"object_id": "obj_water_bottle_500ml", "slot_id": "slot_A"},
    )
    assert resp.status_code == 409, resp.text
    assert resp.json()["detail"] == "No active session"
