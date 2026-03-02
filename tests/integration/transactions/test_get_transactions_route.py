import pytest
from app.models.transaction import Transaction
from app.models.user import User
from bson import ObjectId
from unittest.mock import AsyncMock
from app.main import app
from app.core.auth_dependencies import get_current_user
from app.dependencies.transactions_dependencies import get_list_transaction_use_case
from httpx import ASGITransport, AsyncClient
from fastapi import status
from tests.factories.transaction_factory import transaction_factory
from app.schemas.transaction import TransactionResponse
from datetime import datetime, UTC

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "transactions_input, expected_status", 
    [
        (
            [
                {"amount": 5, "balance_before": 27, "balance_after": 32},
                {"amount": 12, "balance_before": 39, "balance_after": 27},
            ],
            status.HTTP_200_OK
        ),
        (
            [],
            status.HTTP_200_OK
        )
        
    ]
)
async def test_get_route_sucess(client, transactions_input, expected_status):

    # Mock Fake User
    fake_user = User(
        id = ObjectId(),
        email = "test@test.com"
    )

    transactions = [
    TransactionResponse(
        id = str(ObjectId()),
        type = "recharge",
        amount = tx_data["amount"],
        balance_before = tx_data["balance_before"],
        balance_after = tx_data["balance_after"],
        created_at = datetime.now(UTC)
    )
    for tx_data in transactions_input
]

    async def override_get_current_user():
        return fake_user
    
    # Moce Use Case
    mock_use_case = AsyncMock()
    mock_use_case.execute.return_value = transactions

    async def override_get_use_case():
        return mock_use_case
    
    # Overrides
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_list_transaction_use_case] = override_get_use_case

    try:
        response = await client.get("/transactions/")

        # Assertions 
        assert response.status_code == expected_status
        assert response.json()["data"] == [
            tx.model_dump(mode="json") for tx in transactions
        ]

        mock_use_case.execute.assert_called_once_with(fake_user.id)

    finally:
        
        app.dependency_overrides.clear()
