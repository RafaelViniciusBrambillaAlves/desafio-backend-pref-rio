from app.domain.chatbot_intents import ChatbotIntent
from app.services.chatbot_intent_resolver import ChatbotIntentResolver
from app.schemas.chatbot_response import ChatbotResponse, ChatbotResponseType
from app.repositories.interfaces.chatbot_context_repository_interface import IChatbotContextRepository
from app.application.chatbot.handlers.base_handler import BaseChatbotHandler
from bson import ObjectId
from app.domain.chatbot_state import ChatbotState
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork

class HandleChatbotMessageUseCase:

    def __init__(
            self,
            uow : IUnitOfWork,
            handlers: dict[ChatbotIntent, BaseChatbotHandler]         
    ):
        self._uow = uow
        self._handlers = handlers

    async def execute(self, message: str, user_id: ObjectId):

        async with self._uow:      

            context = await self._uow.chatbot_context.get(user_id)

            if context.state != ChatbotState.IDLE:
                handler = self._handlers.get(ChatbotIntent.RECHARGE)
            else:
                intent = ChatbotIntentResolver.resolve(message)
                handler = self._handlers.get(intent)

            if not handler:
                return ChatbotResponse(
                    intent = ChatbotIntent.UNKNOWN,
                    type = ChatbotResponseType.ERROR,
                    message = "Não entendi. Pergunte sobre saldo ou recarga."
                )

            response = await handler.handle(message, user_id, context, self._uow)

            if response.reset_context:
                await self._uow.chatbot_context.reset(user_id)
            
            elif response.next_state:
                context.state = response.next_state

                if response.temp_amount is not None:
                    context.temp_amount = response.temp_amount
                    
                await self._uow.chatbot_context.update(context)
            
            return response