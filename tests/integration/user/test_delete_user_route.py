import pytest
from app.models.user import User
from bson import ObjectId
from unittest.mock import AsyncMock
from app.main import app
from app.core.auth_dependencies import get_current_user
from app.dependencies.user_dependencies import get_delete_user_use_case
from httpx import ASGITransport, AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_delete_user_sucess():

    user_id = ObjectId()

    authenticated_user = User(
        id = user_id,
        email = "test@test.com"
    )

    deleted_user = User(
        id = user_id,
        email = "test@test.com"
    )

    async def override_get_current_user():
        return authenticated_user
    
    mock_use_case  = AsyncMock()
    mock_use_case .execute.return_value = deleted_user

    async def override_use_case():
        return mock_use_case 
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_delete_user_use_case] = override_use_case

    transport = ASGITransport(app = app)

    async with AsyncClient(
        transport = transport,
        base_url = "http://test"
    ) as client:
        response = await client.delete("/users/me")

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["data"]["id"] == str(user_id)
    assert body["data"]["email"] == deleted_user.email

    mock_use_case.execute.assert_called_once_with(user_id)

    app.dependency_overrides.clear()

