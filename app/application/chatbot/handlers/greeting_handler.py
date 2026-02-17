from app.application.chatbot.handlers.base_handler import BaseChatbotHandler
from app.schemas.chatbot_response import ChatbotResponse, ChatbotResponseType
from app.domain.chatbot_intents import ChatbotIntent


class GreetingHandler(BaseChatbotHandler):

    async def handle(self, message, user_id, context):

        return ChatbotResponse(
            intent = ChatbotIntent.GREETING,
            type = ChatbotResponseType.INFO,
            message = "Olá! Posso te ajudar com saldo ou recarga."
        )

