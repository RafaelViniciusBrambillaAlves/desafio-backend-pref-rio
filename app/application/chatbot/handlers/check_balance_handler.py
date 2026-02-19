from app.application.chatbot.handlers.base_handler import BaseChatbotHandler
from app.application.use_cases.transport_pass.get_balance_use_case import GetBalanceUseCase
from app.schemas.chatbot_response import ChatbotResponse, ChatbotResponseType
from app.domain.chatbot_intents import ChatbotIntent


class CheckBalanceHandler(BaseChatbotHandler):

    async def handle(self, message, user_id, context, uow):

        transport_pass = await uow.transport_passes.get_by_user_id(user_id)

        if not transport_pass:
            return ChatbotResponse(
                intent = ChatbotIntent.CHECK_BALANCE,
                type = ChatbotResponseType.INFO,
                message = "Você ainda não possui cartão de transporte."
            )

        return ChatbotResponse(
            intent = ChatbotIntent.CHECK_BALANCE,
            type = ChatbotResponseType.INFO,
            message = f"O seu saldo atual é R${transport_pass.balance:.2f}"
        )
