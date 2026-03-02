import pytest
from app.models.user import User
from bson import ObjectId
from unittest.mock import AsyncMock, patch
from app.application.use_cases.auth.login_with_google_use_case import LoginWithGoogleUseCase
from app.core.exceptions import AppException
from fastapi import status

@pytest.mark.asyncio
async def test_login_google_user_already_exists(mock_uow):
    
    user_id = ObjectId()

    existing_user = User(
        id = user_id,
        email = "test@gmail.com",
        password = None,
        provider = "google"
    )

    mock_uow.users.get_by_email = AsyncMock(return_value = existing_user)

    use_case = LoginWithGoogleUseCase(mock_uow)

    with patch.object(use_case, "_exchange_code_for_token", return_value = {"access_token": "token"}), \
         patch.object(use_case, "_get_user_info", return_value = {"email": "test@gmail.com"}), \
         patch("app.core.jwt.JWTService.create_access_token", return_value = "access-token"), \
         patch("app.core.jwt.JWTService.create_refresh_token", return_value = "refresh-token"):
        
        result = await use_case.execute("fake_code")

    assert result.user.id == str(user_id)
    assert result.user.email == "test@gmail.com"
    assert result.tokens.access_token == "access-token"
    assert result.tokens.refresh_token == "refresh-token"

    mock_uow.users.create.assert_not_called()

@pytest.mark.asyncio
async def test_login_google_creates_new_user(mock_uow):

    user_id = ObjectId()

    mock_uow.users.get_by_email = AsyncMock(return_value = None)

    created_user = User(
        id = user_id,
        email = "new@gmail.com",
        password = None,
        provider = "google"
    )

    mock_uow.users.create = AsyncMock(return_value = created_user)

    use_case = LoginWithGoogleUseCase(mock_uow)

    with patch.object(use_case, "_exchange_code_for_token", return_value = {"access_token": "token"}), \
         patch.object(use_case, "_get_user_info", return_value = {"email": "new@gmail.com"}), \
         patch("app.core.jwt.JWTService.create_access_token", return_value = "access-token"), \
         patch("app.core.jwt.JWTService.create_refresh_token", return_value = "refresh_token"):
        
        result = await use_case.execute("fake_code")

    assert result.user.email == "new@gmail.com"
    
    mock_uow.users.create.assert_called_once()

@pytest.mark.asyncio
async def test_login_google_token_exchange_failure(mock_uow):
    
    use_case = LoginWithGoogleUseCase(mock_uow)

    with patch.object(
            use_case, 
            "_exchange_code_for_token",
            side_effect = AppException(
                error = "GOOGLE_AUTH_FAILED",
                message = "Google authentication failed",
                status_code = status.HTTP_401_UNAUTHORIZED
            )
        ):

        with pytest.raises(AppException):
            await use_case.execute("invalid_code")

@pytest.mark.asyncio
async def test_login_google_user_info_failure(mock_uow):
    
    use_case = LoginWithGoogleUseCase(mock_uow)

    with patch.object(use_case, "_exchange_code_for_token", return_value = {"access_token": "token"}), \
         patch.object(
             use_case,
             "_get_user_info", 
             side_effect = AppException(
                error = "GOOGLE_USER_INFO_FAILED",
                message = "Failed to fetch Google user info",
                status_code = status.HTTP_401_UNAUTHORIZED
            )
        ):
        
        with pytest.raises(AppException):
            await use_case.execute("fake_code")