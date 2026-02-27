import pytest
from unittest.mock import AsyncMock
from bson import ObjectId
from app.models.user import User
from app.application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from app.core.exceptions import AppException
from fastapi import status

@pytest.mark.asyncio
async def test_delete_user_success():

    user_id = str(ObjectId())

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

    deleted_user = User(
        id = ObjectId(),
        email = "test@test.com", 
        password = "hashed"
    )

    mock_uow.users.delete_by_id.return_value = deleted_user

    use_case = DeleteUserUseCase(mock_uow)

    result = await use_case.execute(user_id)

    # Assert
    mock_uow.users.delete_by_id.assert_called_once_with(user_id)

    assert result.email == deleted_user.email

@pytest.mark.asyncio
async def test_delete_user_not_found():

    user_id = str(ObjectId())

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

    mock_uow.users.delete_by_id.return_value = None

    use_case = DeleteUserUseCase(mock_uow)

    with pytest.raises(AppException) as exc:
        await use_case.execute(user_id)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.error == "USER_NOT_FOUND"


