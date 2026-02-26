import pytest
from app.models.user import User
from bson import ObjectId
from unittest.mock import AsyncMock
from app.main import app
from app.core.auth_dependencies import get_current_user
from app.dependencies.transport_pass_dependecies import get_balance_use_case
from httpx import AsyncClient, ASGITransport
from fastapi import status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_balance",
    [0, 10, 200, 999]
)
async def test_get_balance_route_sucess(mock_balance):

    # Mock Fake User
    fake_user = User(
        id = ObjectId(),
        email = "test@test.com"
    )

    async def override_get_current_user():
        return fake_user
    

    # Mock Use Case
    mock_use_case = AsyncMock()
    mock_use_case.execute.return_value = mock_balance

    async def override_get_use_case():
        return mock_use_case
    

    # Overrides
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_balance_use_case] = override_get_use_case

    transport = ASGITransport(app = app)

    async with AsyncClient(
        transport = transport,
        base_url = "http://test"
    ) as client:
        response = await client.get("/transport-pass/balance")

    
    # Asserts
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["balance"] == mock_balance

    mock_use_case.execute.assert_called_once_with(fake_user.id)

    app.dependency_overrides.clear()