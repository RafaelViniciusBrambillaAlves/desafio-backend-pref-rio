import pytest
from bson import ObjectId
from unittest.mock import AsyncMock
from app.models.transport_pass import TransportPass
from app.application.use_cases.transport_pass.use_transport_pass_use_case import UseTransportPassUseCase
from app.core.exceptions import AppException
from fastapi import status

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "initial_balance, debit_amount, expected_balance",
    [
        (10, 7, 3),
        (100, 10, 90), 
        (1, 1, 0),
        (1000, 1, 999)
    ]
)
async def test_use_transport_pass_success(initial_balance, debit_amount, expected_balance):
    user_id = ObjectId()

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

    transport_pass = TransportPass(
        user_id = user_id,
        balance = initial_balance
    )

    updated_pass = TransportPass(
        user_id = user_id,
        balance = expected_balance
    )

    mock_uow.transport_passes.get_by_user_id = AsyncMock(return_value = transport_pass)
    mock_uow.transport_passes.debit_balance = AsyncMock(return_value = updated_pass)

    mock_uow.transactions.create = AsyncMock()

    use_case = UseTransportPassUseCase(mock_uow)

    result = await use_case.execute(user_id, debit_amount)

    assert result == expected_balance

    mock_uow.transport_passes.debit_balance.assert_awaited_once_with(
        user_id = user_id,
        amount = debit_amount
    )

    mock_uow.transactions.create.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "debit_value", 
    [0, -1, -100, -4243]
)
async def test_use_transport_pass_invalid_amount(debit_value):

    user_id = ObjectId()

    mock_uow = AsyncMock()

    use_case = UseTransportPassUseCase(mock_uow)

    with pytest.raises(AppException) as exc:
        await use_case.execute(user_id, debit_value)

    assert exc.value.error == "INVALID_AMOUNT"
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_use_transport_pass_not_found():

    user_id = ObjectId()

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

    mock_uow.transport_passes.get_by_user_id = AsyncMock(return_value = None)

    use_case = UseTransportPassUseCase(mock_uow)

    with pytest.raises(AppException) as exc:
        await use_case.execute(user_id, 10)
    
    assert exc.value.error == "TRANSPORT_PASS_NOT_FOUND"
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "initial_balance, debit_amount",
    [
        (5, 10),
        (100, 101),
        (1, 2),
        (1, 1000)
    ]
)
async def test_use_transport_pass_insufficient_balance(initial_balance, debit_amount):

    user_id = ObjectId()

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

    transport_pass = TransportPass(
        user_id = user_id,
        balance = initial_balance
    )

    mock_uow.transport_passes.get_by_user_id = AsyncMock(return_value = transport_pass)

    use_case = UseTransportPassUseCase(mock_uow)

    with pytest.raises(AppException) as exc:
        await use_case.execute(user_id, debit_amount)

    assert exc.value.error == "INSUFFICIENT_BALANCE"
    assert exc.value.status_code == status.HTTP_409_CONFLICT

    mock_uow.transport_passes.debit_balance.assert_not_called()
    mock_uow.transactions.create.assert_not_called()