import pytest 
from unittest.mock import AsyncMock
from app.application.chatbot.handlers.recharge_handler import RechargeHandler
from app.domain.chatbot_state import ChatbotState
from bson import ObjectId

class FakeContext:
    def __init__(self, state, temp_amount = None):
        self.state = state
        self.temp_amount = temp_amount

@pytest.mark.asyncio
async def test_recharge_cancel_during_amount(mock_uow):
    
    handler = RechargeHandler(AsyncMock())

    context = FakeContext(ChatbotState.WAITING_RECHARGE_AMOUNT)

    response = await handler.handle(
        message = "cancelar",
        user_id = ObjectId(),
        context = context,
        uow = mock_uow
    )

    assert response.reset_context is True
    assert response.message == "Recarga cancelada."

@pytest.mark.asyncio
async def test_recharge_invalid_amount_text(mock_uow):
    
    handler = RechargeHandler(AsyncMock())

    context = FakeContext(ChatbotState.WAITING_RECHARGE_AMOUNT)

    response = await handler.handle(
        message = "gjewgjiew",
        user_id = ObjectId(),
        context = context,
        uow = mock_uow
    )

    assert response.type.name == "ERROR"
    assert response.message == "Informe um valor válido ou cancele."

@pytest.mark.asyncio
async def test_recharge_negative_amount(mock_uow):
    
    handler = RechargeHandler(AsyncMock())

    context = FakeContext(ChatbotState.WAITING_RECHARGE_AMOUNT)

    response = await handler.handle(
        message = "-10",
        user_id = ObjectId(),
        context = context,
        uow = mock_uow
    )

    assert response.type.name == "ERROR"

@pytest.mark.asyncio
async def test_recharge_valid_amount_goes_to_confirm(mock_uow):
    
    handler = RechargeHandler(AsyncMock())

    context = FakeContext(ChatbotState.WAITING_RECHARGE_AMOUNT)

    response = await handler.handle(
        message = "25.50",
        user_id = ObjectId(),
        context = context,
        uow = mock_uow
    )

    assert response.next_state == ChatbotState.CONFIRM_RECHARGE
    assert response.temp_amount == 25.50
    assert "25.50" in response.message

@pytest.mark.asyncio
async def test_recharge_confirm_no(mock_uow):

    handler = RechargeHandler(AsyncMock())

    context = FakeContext(
        ChatbotState.CONFIRM_RECHARGE, 
        temp_amount = 20.0
    )

    response = await handler.handle(
        message = "não",
        user_id = ObjectId(),
        context = context,
        uow = mock_uow
    )

    assert response.reset_context is True
    assert response.message == "Recarga cancelada"

@pytest.mark.asyncio
async def test_recharge_confirm_invalid_answer(mock_uow):
    
    handler = RechargeHandler(AsyncMock())

    context = FakeContext(
        ChatbotState.CONFIRM_RECHARGE,
        temp_amount = 20.0
    )

    response = await handler.handle(
        message = "talvez", 
        user_id = ObjectId(),
        context = context,
        uow = mock_uow
    )

    assert response.type.name == "ERROR"
    assert response.message == "Responda com 'sim' para confirmar e 'não' para cancelar."

@pytest.mark.asyncio
async def test_recharge_confirm_yes_executes_use_case(mock_uow):

    use_case = AsyncMock()
    use_case.execute = AsyncMock(return_value = 150.0)

    handler = RechargeHandler(use_case)

    user_id = ObjectId()

    context = FakeContext(
        ChatbotState.CONFIRM_RECHARGE,
        temp_amount = 30.0
    )

    response = await handler.handle(
        message = "sim",
        user_id = user_id,
        context = context,
        uow = mock_uow
    )

    use_case.execute.assert_called_once_with(
        user_id,
        30.0
    )

    assert response.reset_context is True
    assert response.message == "Recarga realizada. Saldo atual: R$150.00"

@pytest.mark.asyncio
async def test_recharge_starts_from_idle(mock_uow):

    handler = RechargeHandler(mock_uow)

    context = FakeContext(ChatbotState.IDLE)

    response = await handler.handle(
        message = "qualquer coisa",
        user_id = ObjectId(),
        context = context,
        uow = mock_uow
    )

    assert response.type.name == "QUESTION"
    assert response.next_state == ChatbotState.WAITING_RECHARGE_AMOUNT
    assert response.message == "Qual o valor deseja recarregar?"