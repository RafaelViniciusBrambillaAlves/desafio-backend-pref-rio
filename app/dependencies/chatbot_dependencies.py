from fastapi import Depends
from app.dependencies.transport_pass_dependecies import get_recharge_use_case, get_balance_use_case
from app.application.use_cases.chatbot.handle_chatbot_message_use_case import HandleChatbotMessageUseCase
from app.domain.chatbot_intents import ChatbotIntent
from app.application.chatbot.handlers.greeting_handler import GreetingHandler
from app.application.chatbot.handlers.check_balance_handler import CheckBalanceHandler
from app.application.chatbot.handlers.recharge_handler import RechargeHandler
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork
from app.repositories.unit_of_work.mongo_unit_of_work import MongoUnitOfWork
from app.dependencies.document_dependencies import get_unit_of_work

def get_chatbot_use_case(
        uow: IUnitOfWork = Depends(get_unit_of_work),
        recharge_use_case = Depends(get_recharge_use_case)
) -> HandleChatbotMessageUseCase:

    handlers = {
        ChatbotIntent.GREETING: GreetingHandler(),
        ChatbotIntent.CHECK_BALANCE: CheckBalanceHandler(),
        ChatbotIntent.RECHARGE: RechargeHandler(recharge_use_case)
    }

    return HandleChatbotMessageUseCase(
        uow = uow,
        handlers = handlers
    )
    