import pytest
from unittest.mock import AsyncMock
from bson import ObjectId

from app.application.use_cases.transport_pass.get_balance_use_case import GetBalanceUseCase
from app.models.transport_pass import TransportPass

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "existing_balance",
    [0, 10, 150, 999]
)
async def test_get_balance_existing_transport_pass(existing_balance, mock_uow):

    user_id = ObjectId()

    mock_uow.transport_passes.get_by_user_id = AsyncMock(
        return_value = TransportPass(
            user_id = user_id,
            balance = existing_balance
        )
    )

    use_case = GetBalanceUseCase(mock_uow)

    result = await use_case.execute(user_id)

    assert result == existing_balance

    mock_uow.transport_passes.get_by_user_id.assert_awaited_once_with(user_id)
    mock_uow.transport_passes.create.assert_not_called()

@pytest.mark.asyncio
async def test_get_balance_creates_transport_pass_if_not_exists(mock_uow):

    user_id = ObjectId()

    mock_uow.transport_passes.get_by_user_id = AsyncMock(return_value = None)

    mock_uow.transport_passes.create = AsyncMock(
        return_value = TransportPass(
            user_id = user_id,
            balance = 0 
        )
    )
          
    use_case = GetBalanceUseCase(mock_uow)

    result = await use_case.execute(user_id)

    assert result == 0

    mock_uow.transport_passes.create.assert_called_once_with(user_id)

