import pytest 
from unittest.mock import AsyncMock
from app.schemas.auth import TokenResponse
from app.main import app
from app.dependencies.auth_dependencies import get_refresh_token_use_case
from fastapi import status
from app.core.exceptions import AppException


@pytest.mark.asyncio
async def test_refresh_route_success(client):
    
    mock_use_case = AsyncMock()
    mock_use_case.execute = AsyncMock(
        return_value = TokenResponse(
            access_token = "new-access",
            refresh_token = "valid-refresh-token"
        )
    )

    async def override_get_refresh_token_use_case():
        return mock_use_case

    app.dependency_overrides[get_refresh_token_use_case] = override_get_refresh_token_use_case

    response = await client.post(
        "/auth/refresh",
        json = {"refresh_token": "valid-refresh-token"}
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()

    assert body["message"] == "Token refreshed successfully"
    assert body["data"]["access_token"] == "new-access"
    assert body["data"]["refresh_token"] == "valid-refresh-token"
    

@pytest.mark.asyncio
async def test_refresh_route_invalid_token(client):
    
    mock_use_case = AsyncMock()
    mock_use_case.execute = AsyncMock(
        side_effect = AppException(
            error = "INVALID_TOKEN",
            message = "Invalid token",
            status_code = status.HTTP_401_UNAUTHORIZED
        )
    )

    async def override_get_refresh_token_use_case():
        return mock_use_case

    app.dependency_overrides[get_refresh_token_use_case] = override_get_refresh_token_use_case

    response = await client.post(
        "/auth/refresh",
        json = {"refresh_token": "invalid"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED