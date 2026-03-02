import pytest
from app.application.use_cases.user.get_user_use_case import GetUserUseCase
from unittest.mock import AsyncMock
from app.models.user import User
from fastapi import status
from bson import ObjectId
from app.core.exceptions import AppException


@pytest.mark.asyncio
async def test_get_existing_user(mock_uow):
    
    # Fake User
    user_id = str(ObjectId())

    expected_user = User(
        id = ObjectId(user_id),
        email = "test@test.com"
    )

    mock_uow.users.get_by_id = AsyncMock(
        return_value = expected_user
    ) 

    use_case = GetUserUseCase(mock_uow)

    result = await use_case.execute(user_id)

    # Assert
    assert result == expected_user
    mock_uow.users.get_by_id.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_not_existing_user(mock_uow):
    
    user_id = str(ObjectId())

    mock_uow.users.get_by_id = AsyncMock(
        return_value = None
    )

    use_case = GetUserUseCase(mock_uow)

    # Act + Assert
    with pytest.raises(AppException) as exc_info:
        await use_case.execute(user_id)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.error == "USER_NOT_FOUND"

    