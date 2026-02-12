from app.models.chatbot_context import ChatbotContext
from bson import ObjectId
from pymongo import ReturnDocument
from app.repositories.interfaces.chatbot_context_repository_interface import IChatbotContextRepository

class ChatbotContextRepository(IChatbotContextRepository):

    def __init__(self, database):
        self.db = database

    async def get(self, user_id: ObjectId) -> ChatbotContext:
        data = await self.db.chatbot_context.find_one({"user_id": user_id})

        if data:
            return ChatbotContext(**data)
        
        context = ChatbotContext(user_id = user_id)
        await self.db.chatbot_context.insert_one(context.model_dump( by_alias = True))
        return context

    async def update(self, context: ChatbotContext) -> ChatbotContext:
        data = await self.db.chatbot_context.find_one_and_update(
            {"user_id": context.user_id}, 
            {"$set": context.model_dump(by_alias = True)},
            return_document = ReturnDocument.AFTER 
        ) 
        return ChatbotContext(**data)
    
    async def reset(self, user_id: ObjectId):
        await self.db.chatbot_context.delete_one({"user_id": user_id})