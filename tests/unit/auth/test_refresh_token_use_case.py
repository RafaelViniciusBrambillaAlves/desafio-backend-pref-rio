import pytest
from unittest.mock import AsyncMock, patch
from app.application.use_cases.auth.refresh_token_use_case import RefreshTokenUseCase
from app.core.exceptions import AppException
from fastapi import status
from bson import ObjectId
from app.models.user import User

@pytest.mark.asyncio
async def test_refresh_token_success(mock_uow):
    
    user_id = ObjectId()

    mock_uow.users.get_by_id = AsyncMock(
        return_value = User(
            id = user_id,
            email = "test@test.com",
            password = "hashed",
            provider = "local"
        )
    )

    use_case = RefreshTokenUseCase(mock_uow)

    with patch("app.core.jwt.JWTService.decode_token", return_value = {
        "type": "refresh",
        "sub": user_id
    }), patch("app.core.jwt.JWTService.create_access_token", return_value = "new-access-token"
    ):
        result = await use_case.execute("valid_refresh_token")

        assert result.access_token == "new-access-token"
        assert result.refresh_token == "valid_refresh_token"

@pytest.mark.asyncio
async def test_refresh_token_invalid_token_type(mock_uow):
    
    use_case = RefreshTokenUseCase(mock_uow)

    with patch("app.core.jwt.JWTService.decode_token", return_value = {
        "type": "access",
        "sub": "some_id"
    }):
        with pytest.raises(AppException) as exc: 
            await use_case.execute("invalid_refresh_token")

        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.error == "INVALID_TOKEN_TYPE"

@pytest.mark.asyncio
async def test_refresh_token_user_not_found(mock_uow):

    mock_uow.users.get_by_id = AsyncMock(return_value = None)
    
    use_case = RefreshTokenUseCase(mock_uow)

    with patch("app.core.jwt.JWTService.decode_token", return_value = {
        "type": "refresh",
        "sub": "not_existent_user"
    }):

        with pytest.raises(AppException) as exc:
            await use_case.execute("invalid_refresh_token")

        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.error == "USER_NOT_FOUND"


