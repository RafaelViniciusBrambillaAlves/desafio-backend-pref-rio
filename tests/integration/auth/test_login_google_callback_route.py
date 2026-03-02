import pytest
from unittest.mock import AsyncMock
from app.schemas.auth import LoginResponse, UserPublic, TokenResponse
from app.dependencies.auth_dependencies import get_google_login_use_case
from fastapi import status
from bson import ObjectId
from app.main import app
from app.core.exceptions import AppException

@pytest.mark.asyncio
async def test_google_callback_success(client):

    mock_use_case = AsyncMock()

    mock_use_case.execute = AsyncMock(
        return_value = LoginResponse(
            user = UserPublic(
                id = str(ObjectId()),
                email = "test@test.com"
            ),
            tokens = TokenResponse(
                access_token = "access-token",
                refresh_token = "refresh-token"
            )
        )
    )

    async def override_get_google_login_use_case():
        return mock_use_case
    
    app.dependency_overrides[get_google_login_use_case] = override_get_google_login_use_case

    response = await client.get(
        "/auth/google/callback?code=fake-code"
    )    

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["message"] == "Login with Google successfully"
    assert body["data"]["user"]["email"] == "test@test.com"
    assert body["data"]["tokens"]["access_token"] == "access-token"    

@pytest.mark.asyncio
async def test_google_callback_failure(client):

    mock_use_case = AsyncMock()
    mock_use_case.execute = AsyncMock(
        side_effect = AppException(
            error = "GOOGLE_FAILED",
            message = "Google failed",
            status_code = status.HTTP_401_UNAUTHORIZED
        )
    )

    async def override_get_google_login_use_case():
        return mock_use_case
    
    app.dependency_overrides[get_google_login_use_case] = override_get_google_login_use_case

    response = await client.get(
        "/auth/google/callback?code=invalid"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED