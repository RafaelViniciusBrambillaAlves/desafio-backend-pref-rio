import pytest 
from bson import ObjectId
from unittest.mock import AsyncMock, patch
from app.application.use_cases.auth.login_user_use_case import LoginUserUseCase
from app.core.exceptions import AppException
from fastapi import status

class FakeUser:
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

@pytest.mark.asyncio
async def test_login_success(mock_uow):
    
    user_id = ObjectId()
    email = "test@test.com"
    password = "123456"
    hashed_password = "hashed"

    fake_user = FakeUser(user_id, email, hashed_password)

    mock_uow.users.get_by_email = AsyncMock(return_value = fake_user)

    use_case = LoginUserUseCase(mock_uow)

    with patch("app.core.security.Security.verify_password", return_value = True), \
         patch("app.core.jwt.JWTService.create_access_token", return_value = "access-token"), \
         patch("app.core.jwt.JWTService.create_refresh_token", return_value = "refresh-token"):
        
        result = await use_case.execute(email, password)

        assert result.user.email == email
        assert result.tokens.access_token == "access-token"
        assert result.tokens.refresh_token == "refresh-token"

        mock_uow.users.get_by_email.assert_awaited_once_with(email)


@pytest.mark.asyncio
async def test_login_user_not_found(mock_uow):
    
    mock_uow.users.get_by_email = AsyncMock(return_value = None)

    use_case = LoginUserUseCase(mock_uow)

    with pytest.raises(AppException) as exc:
        await use_case.execute("test@test.com", "123456")

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.error == "INVALID_CREDENTIALS"


@pytest.mark.asyncio
async def test_login_user_without_password(mock_uow):
    
    fake_user = FakeUser(ObjectId(), "test@test.com", None)

    mock_uow.users.get_by_email = AsyncMock(return_value = fake_user)

    use_case = LoginUserUseCase(mock_uow)

    with pytest.raises(AppException) as exc:
        await use_case.execute("test@test.com", "123456")

    print("EXC: ", exc)
    print("EXC.VALUE: ", exc.value)
    print("EXC.VALUE.ERROR: ", exc.value.error)

@pytest.mark.asyncio
async def test_login_user_invalid_password(mock_uow):
    
    fake_user = FakeUser(ObjectId(), "test@test.com", "hashed")

    mock_uow.users.get_by_email = AsyncMock(return_value = fake_user)

    use_case = LoginUserUseCase(mock_uow)

    with patch("app.core.security.Security.verify_password", return_value = None):

        with pytest.raises(AppException) as exc:
            await use_case.execute("test@test.com", "wrong_password")
        
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.error == "INVALID_CREDENTIALS"

