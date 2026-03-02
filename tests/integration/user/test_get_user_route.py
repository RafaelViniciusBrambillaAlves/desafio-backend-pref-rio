import pytest
from app.models.user import User
from bson import ObjectId
from unittest.mock import AsyncMock
from app.main import app
from app.core.auth_dependencies import get_current_user
from app.dependencies.user_dependencies import get_get_user_use_case
from httpx import ASGITransport, AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_get_route_success(client):

    fake_authenticated_user  = User(
        id = ObjectId(),
        email = "test@test.com"
    )

    user_id = ObjectId()

    returned_user = User(
        id = user_id,
        email = "user@email.com"
    )

    async def override_get_current_user():
        return fake_authenticated_user
    
    mock_use_case = AsyncMock()
    mock_use_case.execute.return_value = returned_user

    async def override_get_use_case():
        return mock_use_case

    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_get_user_use_case] = override_get_use_case

    try:
        response = await client.get(f"/users/{str(user_id)}")

    
        assert response.status_code == status.HTTP_200_OK
        
        body = response.json()

        assert body["data"]["id"] == str(user_id)
        assert body["data"]["email"] == returned_user.email

        mock_use_case.execute.assert_called_once_with(str(user_id))

    finally:

        app.dependency_overrides.clear()



