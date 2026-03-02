import pytest
from app.application.use_cases.user.create_user_use_case import CreateUserUseCase
from bson import ObjectId
from app.schemas.user import UserReponse, UserCreate
from unittest.mock import AsyncMock
from app.main import app
from app.dependencies.user_dependencies import get_create_user_use_case
from httpx import ASGITransport, AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_create_user_success(client):

    user_payload = {
        "email": "test@test.com",
        "password": "123456"
    }

    created_user = AsyncMock()
    created_user.id = ObjectId()
    created_user.email = "test@test.com"

    mock_use_case = AsyncMock()
    mock_use_case.execute.return_value = created_user

    async def override_get_create_user_use_case():
        return mock_use_case
    
    app.dependency_overrides[get_create_user_use_case] = override_get_create_user_use_case

    try:
        response = await client.post(
            "/users/",
            json = user_payload
        )

        assert response.status_code == status.HTTP_201_CREATED
        
        body = response.json()

        assert body["data"]["email"] == user_payload["email"]
        assert body["data"]["id"] is not None
        
        mock_use_case.execute.assert_called_once()
    
    finally:

        app.dependency_overrides.clear()