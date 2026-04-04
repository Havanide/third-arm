"""
tests/integration/test_artifact_inspection.py
─────────────────────────────────────────────────────────────────────────────
Integration tests for GET /artifacts/{session_id}.

Covers:
  - happy path: full flow produces a closed bundle, endpoint returns full metadata
  - not found: 404 for unknown session_id
  - partial bundle: bundle dir with only manifest.json returns degraded response
"""

from __future__ import annotations

import json

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from third_arm.core.settings import get_settings
from third_arm.main import create_app


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest_asyncio.fixture
async def client(tmp_path, monkeypatch):
    """AsyncClient with isolated sessions directory."""
    monkeypatch.setenv("THIRD_ARM_SESSIONS_DIR", str(tmp_path))
    get_settings.cache_clear()
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        async with app.router.lifespan_context(app):
            yield ac


@pytest.mark.asyncio
async def test_artifact_inspection_happy_path(client, tmp_path):
    """GET /artifacts/{session_id} returns full metadata for a closed bundle."""

    # Run the full operator flow to produce a closed bundle
    await client.post("/arm/home")
    resp = await client.post(
        "/session/start",
        json={
            "operator_id": "test_op",
            "object_id": "obj_water_bottle_500ml",
            "slot_id": "slot_A",
        },
    )
    assert resp.status_code == 200, resp.text
    session_id = resp.json()["session_id"]

    await client.post(
        "/handover/request",
        json={"object_id": "obj_water_bottle_500ml", "slot_id": "slot_A"},
    )
    await client.post("/session/stop")

    # Inspect the bundle
    resp = await client.get(f"/artifacts/{session_id}")
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["session_id"] == session_id
    assert data["schema_version"] == "1.0"
    assert data["created_at"] is not None
    assert data["closed_at"] is not None
    assert data["is_closed"] is True
    assert data["presence"] == {"manifest": True, "trace": True, "telemetry": True}
    assert data["errors"] == []

    # All three expected files must exist with size_bytes reported
    files_by_name = {f["name"]: f for f in data["files"]}
    assert set(files_by_name) == {"manifest.json", "session_trace.ndjson", "telemetry.mcap"}
    for name, entry in files_by_name.items():
        assert entry["exists"] is True, f"{name} should exist"
        assert "size_bytes" in entry, f"{name} should have size_bytes"

    # Trace summary: at least 5 events (session_started + 3 handover + session_stopped)
    assert data["trace_summary"]["event_count"] >= 5


@pytest.mark.asyncio
async def test_artifact_inspection_not_found(client):
    """GET /artifacts/{session_id} returns 404 for an unknown session."""
    resp = await client.get("/artifacts/session_does_not_exist")
    assert resp.status_code == 404, resp.text
    assert "not found" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_artifact_inspection_partial_bundle(client, tmp_path):
    """GET /artifacts/{session_id} returns degraded response for incomplete bundle."""

    # Create a bundle dir with only a minimal manifest.json (no trace, no mcap)
    session_id = "session_partial"
    bundle_dir = tmp_path / session_id
    bundle_dir.mkdir()
    manifest = {
        "schema_version": "1.0",
        "session_id": session_id,
        "created_at": "2026-04-04T00:00:00Z",
        "closed_at": None,
        "files": {"trace": "session_trace.ndjson", "mcap": "telemetry.mcap"},
    }
    (bundle_dir / "manifest.json").write_text(json.dumps(manifest))

    resp = await client.get(f"/artifacts/{session_id}")
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["session_id"] == session_id
    assert data["is_closed"] is False
    assert data["closed_at"] is None
    assert data["presence"] == {"manifest": True, "trace": False, "telemetry": False}
    assert data["errors"] == []

    files_by_name = {f["name"]: f for f in data["files"]}
    assert files_by_name["manifest.json"]["exists"] is True
    assert files_by_name["session_trace.ndjson"]["exists"] is False
    assert files_by_name["telemetry.mcap"]["exists"] is False

    # Trace summary event count is 0 for missing trace file
    assert data["trace_summary"]["event_count"] == 0


@pytest.mark.asyncio
async def test_artifact_inspection_missing_manifest_returns_degraded_response(client, tmp_path):
    """Existing bundle dir without manifest remains inspectable as a degraded bundle."""

    session_id = "session_missing_manifest"
    bundle_dir = tmp_path / session_id
    bundle_dir.mkdir()
    (bundle_dir / "session_trace.ndjson").write_text("")

    resp = await client.get(f"/artifacts/{session_id}")
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["session_id"] == session_id
    assert data["schema_version"] is None
    assert data["presence"] == {"manifest": False, "trace": True, "telemetry": False}
    assert data["errors"] == ["manifest_missing"]


@pytest.mark.asyncio
async def test_artifact_inspection_malformed_manifest_returns_degraded_response(client, tmp_path):
    """Malformed manifest should not collapse into a misleading 404."""

    session_id = "session_bad_manifest"
    bundle_dir = tmp_path / session_id
    bundle_dir.mkdir()
    (bundle_dir / "manifest.json").write_text("{not-json")

    resp = await client.get(f"/artifacts/{session_id}")
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["session_id"] == session_id
    assert data["schema_version"] is None
    assert data["presence"] == {"manifest": True, "trace": False, "telemetry": False}
    assert data["errors"] == ["manifest_unreadable"]


@pytest.mark.asyncio
async def test_artifact_inspection_rejects_unsafe_session_id(client):
    """Path traversal style session ids must not escape the sessions directory."""

    resp = await client.get("/artifacts/..")
    assert resp.status_code == 404, resp.text
    assert "not found" in resp.json()["detail"].lower()
