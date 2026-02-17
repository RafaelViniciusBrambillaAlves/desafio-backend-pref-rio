from app.application.chatbot.handlers.base_handler import BaseChatbotHandler
from app.application.use_cases.transport_pass.get_balance_use_case import GetBalanceUseCase
from app.schemas.chatbot_response import ChatbotResponse, ChatbotResponseType
from app.domain.chatbot_intents import ChatbotIntent


class CheckBalanceHandler(BaseChatbotHandler):
    
    def __init__(self, get_balance_use_case: GetBalanceUseCase):
        self._get_balance_user_case = get_balance_use_case

    async def handle(self, message, user_id, context):

        balance = await self._get_balance_user_case.execute(user_id)

        return ChatbotResponse(
            intent = ChatbotIntent.CHECK_BALANCE,
            type = ChatbotResponseType.INFO,
            message = f"O seu saldo atual é R${balance:.2f}"
        )
