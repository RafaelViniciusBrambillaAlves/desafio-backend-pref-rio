import pytest
from bson import ObjectId
from unittest.mock import AsyncMock
from app.domain.chatbot_state import ChatbotState
from app.application.use_cases.chatbot.handle_chatbot_message_use_case import HandleChatbotMessageUseCase
from app.domain.chatbot_intents import ChatbotIntent

@pytest.mark.asyncio
async def test_unknown_intent_returns_error(mock_uow):

    mock_uow.chatbot_context.get = AsyncMock()

    context = AsyncMock()
    context.state = ChatbotState.IDLE

    mock_uow.chatbot_context.get.return_value = context

    use_case = HandleChatbotMessageUseCase(
        uow = mock_uow,
        handlers = {}
    )

    response = await use_case.execute(
        message = "gfdjgsjioewrio", 
        user_id = ObjectId()
    )

    assert response.type.name == "ERROR"

@pytest.mark.asyncio
async def test_handle_message_resets_context(mock_uow):
    
    user_id = ObjectId()

    context = AsyncMock()

    context.state = ChatbotState.IDLE

    mock_uow.chatbot_context.get = AsyncMock(return_value = context)
    mock_uow.chatbot_context.reset = AsyncMock()

    fake_response = AsyncMock()
    fake_response.reset_context = True
    fake_response.next_state = None 

    handler = AsyncMock()

    handler.handle = AsyncMock(return_value = fake_response)

    use_case = HandleChatbotMessageUseCase(
        uow = mock_uow,
        handlers = {ChatbotIntent.RECHARGE: handler}
    )

    await use_case.execute("recarga", user_id)

    mock_uow.chatbot_context.reset.assert_called_once_with(user_id)

@pytest.mark.asyncio
async def test_handle_message_updates_state(mock_uow):
    
    user_id = ObjectId()

    context = AsyncMock()
    context.state = ChatbotState.IDLE

    mock_uow.chatbot_context.get = AsyncMock(return_value = context)
    mock_uow.chatbot_context.update = AsyncMock()

    fake_response = AsyncMock()
    fake_response.reset_context = False
    fake_response.next_state = ChatbotState.WAITING_RECHARGE_AMOUNT
    fake_response.temp_amount = None

    handler = AsyncMock()

    handler.handle = AsyncMock(return_value = fake_response)

    use_case = HandleChatbotMessageUseCase(
        uow = mock_uow,
        handlers = {ChatbotIntent.RECHARGE: handler}
    )

    await use_case.execute("recarga", user_id)

    assert context.state == ChatbotState.WAITING_RECHARGE_AMOUNT
    mock_uow.chatbot_context.update.assert_called_once_with(context)


@pytest.mark.asyncio
async def test_handle_message_updates_state_and_temp_amount(mock_uow):
    
    user_id = ObjectId()

    context = AsyncMock()
    context.state = ChatbotState.IDLE
    context.temp_amount = None

    mock_uow.chatbot_context.get = AsyncMock(return_value = context)
    mock_uow.chatbot_context.update = AsyncMock()

    fake_response = AsyncMock()
    fake_response.reset_context = False
    fake_response.next_state = ChatbotState.CONFIRM_RECHARGE
    fake_response.temp_amount = 50.0

    handler = AsyncMock()
    handler.handle = AsyncMock(return_value = fake_response)

    use_case = HandleChatbotMessageUseCase(
        uow = mock_uow,
        handlers = {ChatbotIntent.RECHARGE: handler}
    )

    await use_case.execute("recarga", user_id)

    assert context.state == ChatbotState.CONFIRM_RECHARGE
    assert context.temp_amount == 50.0

    mock_uow.chatbot_context.update.assert_called_once_with(context)



