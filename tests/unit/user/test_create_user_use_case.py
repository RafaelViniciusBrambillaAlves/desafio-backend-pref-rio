import pytest
from unittest.mock import AsyncMock
from app.models.user import User
from app.application.use_cases.user.create_user_use_case import CreateUserUseCase
from app.schemas.user import UserCreate
from app.core.exceptions import AppException
from fastapi import status
from app.core.security import Security


@pytest.mark.asyncio
async def test_create_user_success():
    
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

    mock_uow.users.get_by_email.return_value = None

    created_user = User(email = "test@test.com", password = "hashed")
    mock_uow.users.create.return_value = created_user

    use_case = CreateUserUseCase(mock_uow)

    user_data = UserCreate(
        email = "test@test.com",
        password = "123456"
    )

    result = await use_case.execute(user_data)

        
    mock_uow.users.get_by_email.assert_called_once_with("test@test.com")
    mock_uow.users.create.assert_called_once()

    assert result.email == "test@test.com"


@pytest.mark.asyncio
async def test_create_user_email_invalid():
    
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

    existing_user = User(email = "test@test.com", password = "hashed")

    mock_uow.users.get_by_email.return_value = existing_user

    use_case = CreateUserUseCase(mock_uow)

    user_data = UserCreate(
        email = "test@test.com",
        password = "123456"
    )

    with pytest.raises(AppException) as exc:
        await use_case.execute(user_data)
    
    assert exc.value.status_code == status.HTTP_409_CONFLICT
    assert exc.value.error == "EMAIL_ALREADY_EXISTS"


@pytest.mark.asyncio
async def test_create_user_password_is_hashed():
    
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

    mock_uow.users.get_by_email.return_value = None

    async def create_side_effect(user):
        return user
    
    mock_uow.users.create.side_effect = create_side_effect

    use_case = CreateUserUseCase(mock_uow)

    user_data = UserCreate(
        email = "test@test.com",
        password = "123456"
    )

    result = await use_case.execute(user_data)

    assert result.password != "123456"
    assert Security.verify_password("123456", result.password)