from fastapi import Depends
from app.dependencies.database_dependencies import get_database
from app.dependencies.transport_pass_dependecies import get_recharge_use_case, get_balance_use_case
from app.application.use_cases.chatbot.handle_chatbot_message_use_case import HandleChatbotMessageUseCase
from app.repositories.interfaces.chatbot_context_repository_interface import IChatbotContextRepository
from app.repositories.chatbot_context_repository import ChatbotContextRepository
from app.domain.chatbot_intents import ChatbotIntent

from app.application.chatbot.handlers.greeting_handler import GreetingHandler
from app.application.chatbot.handlers.check_balance_handler import CheckBalanceHandler
from app.application.chatbot.handlers.recharge_handler import RechargeHandler

def get_chatbot_use_case(
        db = Depends(get_database),
        recharge_use_case = Depends(get_recharge_use_case),
        balance_use_case = Depends(get_balance_use_case)
) -> HandleChatbotMessageUseCase:
    
    context_repository: IChatbotContextRepository = ChatbotContextRepository(db)

    handlers = {
        ChatbotIntent.GREETING: GreetingHandler(),
        ChatbotIntent.CHECK_BALANCE: CheckBalanceHandler(balance_use_case),
        ChatbotIntent.RECHARGE: RechargeHandler(
            recharge_use_case,
            context_repository
        )
    }

    return HandleChatbotMessageUseCase(
        context_repository = context_repository,
        handlers = handlers
    )
    