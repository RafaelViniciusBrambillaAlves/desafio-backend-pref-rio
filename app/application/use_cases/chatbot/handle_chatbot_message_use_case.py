from app.domain.chatbot_intents import ChatbotIntent
from app.services.chatbot_intent_resolver import ChatbotIntentResolver
from app.schemas.chatbot_response import ChatbotResponse, ChatbotResponseType
from app.repositories.interfaces.chatbot_context_repository_interface import IChatbotContextRepository
from app.application.chatbot.handlers.base_handler import BaseChatbotHandler
from bson import ObjectId
from app.domain.chatbot_state import ChatbotState

class HandleChatbotMessageUseCase:

    def __init__(
            self,
            context_repository: IChatbotContextRepository,
            handlers: dict[ChatbotIntent, BaseChatbotHandler]         
    ):
        self._context_repository = context_repository
        self._handlers = handlers

    async def execute(self, message: str, user_id: ObjectId):
        
        context = await self._context_repository.get(user_id)

        if context.state != ChatbotState.IDLE:
            recharge_handler = self._handlers.get(ChatbotIntent.RECHARGE)

            if recharge_handler:
                return await recharge_handler.handle(message, user_id, context)

        intent = ChatbotIntentResolver.resolve(message)

        handler = self._handlers.get(intent)

        if not handler:
            return ChatbotResponse(
                intent = ChatbotIntent.UNKNOWN,
                type = ChatbotResponseType.ERROR,
                message = "Não entendi. Você pode perguntar sobre saldo ou recarga."
            )    
        
        return await handler.handle(message, user_id, context)
        