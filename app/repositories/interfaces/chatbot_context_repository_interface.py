from abc import ABC, abstractmethod
from bson import ObjectId
from app.models.chatbot_context import ChatbotContext

class IChatbotContextRepository(ABC):

    @abstractmethod
    async def get(self, user_id: ObjectId) -> ChatbotContext:
        pass

    @abstractmethod
    async def update(self, context: ChatbotContext) -> ChatbotContext:
        pass

    @abstractmethod
    async def reset (self, user_id: ObjectId) -> None:
        pass