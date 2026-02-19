from app.models.chatbot_context import ChatbotContext
from bson import ObjectId
from pymongo import ReturnDocument
from app.repositories.interfaces.chatbot_context_repository_interface import IChatbotContextRepository
from app.repositories.base_repository import BaseMongoRepository

class ChatbotContextRepository(BaseMongoRepository, IChatbotContextRepository):

    def __init__(self, database):
        super().__init__(database)

    async def get(self, user_id: ObjectId) -> ChatbotContext:
        data = await self._db.chatbot_context.find_one(
            {"user_id": user_id}, 
            session = self._session
        )

        if data:
            return ChatbotContext(**data)
        
        context = ChatbotContext(user_id = user_id)
        await self._db.chatbot_context.insert_one(
            context.model_dump( by_alias = True), 
            session = self._session
        )

        return context

    async def update(self, context: ChatbotContext) -> ChatbotContext:
        data = await self._db.chatbot_context.find_one_and_update(
            {"user_id": context.user_id}, 
            {"$set": context.model_dump(by_alias = True)},
            return_document = ReturnDocument.AFTER,
            session = self._session
        ) 
        return ChatbotContext(**data)
    
    async def reset(self, user_id: ObjectId):
        await self._db.chatbot_context.delete_one(
            {"user_id": user_id},
            session = self._session
            )