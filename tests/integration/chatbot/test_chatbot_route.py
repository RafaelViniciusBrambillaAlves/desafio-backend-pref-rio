import pytest 
from unittest.mock import AsyncMock
from app.models.user import User
from bson import ObjectId
from app.schemas.chatbot_response import ChatbotResponse, ChatbotResponseType
from app.domain.chatbot_intents import ChatbotIntent
from app.core.auth_dependencies import get_current_user
from app.dependencies.chatbot_dependencies import get_chatbot_use_case
from app.main import app
from fastapi import status

@pytest.mark.asyncio
async def test_post_chatbot_message_success(client):
    
    fake_user = User(
        id = ObjectId(),
        email = "test@test.com"
    )

    fake_reponse = ChatbotResponse(
        intent = ChatbotIntent.RECHARGE,
        type = ChatbotResponseType.INFO,
        message = "Resposta Fake",
        next_state = None,
        reset_context = False,
        temp_amount = 50.0
    )

    mock_use_case = AsyncMock()
    mock_use_case.execute = AsyncMock(return_value = fake_reponse)

    async def override_get_current_user():
        return fake_user

    async def override_get_chatbot_use_case():
        return mock_use_case

    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_chatbot_use_case] = override_get_chatbot_use_case

    response = await client.post(
        "/chatbot/message",
        json = {"message": "oi"}
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["message"] == "Chatbot response generated successfully"
    assert body["data"]["message"] == "Resposta Fake"

    mock_use_case.execute.assert_called_once_with(
        "oi",
        fake_user.id
    )

    app.dependency_overrides.clear()
