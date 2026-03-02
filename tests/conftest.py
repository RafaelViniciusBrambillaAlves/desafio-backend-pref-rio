import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import AsyncMock

@pytest_asyncio.fixture
async def client():

    transport = ASGITransport(app = app)

    async with AsyncClient(
        transport = transport,
        base_url = "http://test"
    ) as client:
        yield client

@pytest.fixture
def mock_uow():
    uow = AsyncMock()
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = None
    return uow
