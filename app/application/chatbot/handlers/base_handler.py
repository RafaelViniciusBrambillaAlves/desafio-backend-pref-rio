from abc import ABC, abstractmethod
from bson import ObjectId
from app.models.chatbot_context import ChatbotContext
from app.schemas.chatbot_response import ChatbotResponse

class BaseChatbotHandler(ABC):

    @abstractmethod
    async def handle(
        self, 
        message: str,
        user_id: ObjectId,
        context: ChatbotContext
    ) -> ChatbotResponse:
        pass

