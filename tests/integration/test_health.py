"""
tests/integration/test_health.py
─────────────────────────────────────────────────────────────────────────────
Integration test: start the FastAPI app and exercise the HTTP endpoints.
"""

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
async def client():
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Trigger lifespan startup
        async with app.router.lifespan_context(app):
            yield ac


@pytest.mark.asyncio
async def test_health_ok(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True


@pytest.mark.asyncio
async def test_status_ok(client):
    resp = await client.get("/status")
    assert resp.status_code == 200
    data = resp.json()
    assert "arm_state" in data
    assert data["mock_mode"] is True


@pytest.mark.asyncio
async def test_artifacts_ok(client):
    resp = await client.get("/artifacts")
    assert resp.status_code == 200
    data = resp.json()
    assert "bundles" in data
