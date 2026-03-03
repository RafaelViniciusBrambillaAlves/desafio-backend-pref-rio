import pytest 
from app.application.chatbot.handlers.greeting_handler import GreetingHandler
from bson import ObjectId
from app.domain.chatbot_intents import ChatbotIntent

@pytest.mark.asyncio
async def test_greeting_handler_returns_message(mock_uow):

    handler = GreetingHandler()

    response = await handler.handle(
        message = "oi",
        user_id = ObjectId(),
        context = None,
        uow = mock_uow
    )

    assert response.intent == ChatbotIntent.GREETING
    assert response.message is not None