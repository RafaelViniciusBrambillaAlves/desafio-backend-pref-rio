from abc import ABC, abstractmethod
from bson import ObjectId
from app.models.chatbot_context import ChatbotContext
from app.schemas.chatbot_response import ChatbotResponse
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork

class BaseChatbotHandler(ABC):

    @abstractmethod
    async def handle(
        self, 
        message: str,
        user_id: ObjectId,
        context: ChatbotContext,
        uow: IUnitOfWork
    ) -> ChatbotResponse:
        pass

