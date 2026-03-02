import pytest
from bson import ObjectId
from app.schemas.user import UserPublic
from app.schemas.auth import LoginResponse, TokenResponse
from app.application.use_cases.auth.login_user_use_case import LoginUserUseCase 
from unittest.mock import AsyncMock
from httpx import ASGITransport, AsyncClient
from fastapi import status
from app.main import app
from app.dependencies.auth_dependencies import get_login_use_case

@pytest.mark.asyncio
async def test_login_success(client):

    login_payload = {
        "email": "test@test.com",
        "password": "123456"
    }

    fake_response = {
        "user": {
            "id": str(ObjectId()),
            "email": "test@test.com"
        },
        "tokens": {
            "access_token": "access-token",
            "refresh_token": "refresh-token",
            "token_type": "bearer"
        }
    }

    mock_use_case = AsyncMock(spec = LoginUserUseCase)
    mock_use_case.execute = AsyncMock(return_value = fake_response)

    async def override_get_use_case():
        return mock_use_case
    
    app.dependency_overrides[get_login_use_case] = override_get_use_case
 
    try:
        response = await client.post(
            "/auth/login",
            json = login_payload
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

        body = response.json()

        assert body["message"] == "Login successful."
        assert body["data"]["user"]["email"] == login_payload["email"] 
        assert body["data"]["tokens"]["access_token"] == "access-token"
        assert body["data"]["tokens"]["refresh_token"] == "refresh-token"
        assert body["data"]["tokens"]["token_type"] == "bearer"

        mock_use_case.execute.assert_awaited_once_with(
            login_payload["email"],
            login_payload["password"]
        )
    
    finally:

        app.dependency_overrides.clear()

