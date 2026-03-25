import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from third_arm.core.settings import get_settings
from third_arm.domain.object_model import clear_object_catalog_cache
from third_arm.domain.slot_model import clear_slot_catalog_cache
from third_arm.main import create_app


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    clear_object_catalog_cache()
    clear_slot_catalog_cache()
    yield
    get_settings.cache_clear()
    clear_object_catalog_cache()
    clear_slot_catalog_cache()


@pytest_asyncio.fixture
async def client():
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        async with app.router.lifespan_context(app):
            yield ac


@pytest.mark.asyncio
async def test_unknown_object_rejected_on_session_start(client):
    resp = await client.post('/session/start', json={'object_id': 'obj_missing', 'slot_id': 'slot_A'})
    assert resp.status_code == 404
    assert 'Unknown object_id' in resp.text


@pytest.mark.asyncio
async def test_unknown_slot_rejected_on_session_start(client):
    resp = await client.post('/session/start', json={'object_id': 'obj_mug_ceramic', 'slot_id': 'slot_missing'})
    assert resp.status_code == 404
    assert 'Unknown slot_id' in resp.text
