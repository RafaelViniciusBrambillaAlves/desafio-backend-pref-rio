import pytest
from unittest.mock import AsyncMock
from app.application.chatbot.handlers.check_balance_handler import CheckBalanceHandler
from bson import ObjectId

@pytest.mark.asyncio
async def test_check_balance_without_transport_pass(mock_uow):

    mock_uow.transport_passes.get_by_user_id = AsyncMock(return_value=None)

    handler = CheckBalanceHandler()

    response = await handler.handle(
        message = "saldo",
        user_id = ObjectId(),
        context = None,
        uow = mock_uow
    )

    assert response.message == "Você ainda não possui cartão de transporte."

@pytest.mark.asyncio
async def test_check_balance_with_transport_pass(mock_uow):

    transport_pass = AsyncMock()

    transport_pass.balance = 50.0

    mock_uow.transport_passes.get_by_user_id = AsyncMock(
        return_value = transport_pass
    )

    handler = CheckBalanceHandler()

    response = await handler.handle(
        message = "saldo",
        user_id = ObjectId(),
        context = None,
        uow = mock_uow
    )

    assert response.message == f"O seu saldo atual é R$50.00"