import pytest
from bson import ObjectId
from unittest.mock import AsyncMock
from app.models.transaction import Transaction
from app.application.use_cases.transaction.list_transactions_use_case import ListTransactionsUseCase
from tests.factories.transaction_factory import transaction_factory

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transactions_input", 
    [
        [
            {"amount": 5, "balance_before": 27, "balance_after": 32},
            {"amount": 12, "balance_before": 39, "balance_after": 27},
        ],
        [

        ]
    ]
)
async def test_list_transactions(transactions_input):
    
    user_id = ObjectId()

    # Fake Data
    transactions = [
        transaction_factory(**tx_data) for tx_data in transactions_input
    ]

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

    mock_uow.transactions.list_by_user = AsyncMock(
        return_value = transactions
    )

    use_case = ListTransactionsUseCase(mock_uow)

    result = await use_case.execute(user_id)

    assert len(result) == len(transactions)

    if transactions_input:
        assert result[0].amount == transactions_input[0]["amount"]

    mock_uow.transactions.list_by_user.assert_awaited_once_with(user_id)
    mock_uow.transactions.create.assert_not_called()
    