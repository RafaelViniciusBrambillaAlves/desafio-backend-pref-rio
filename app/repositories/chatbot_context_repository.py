from app.core.database import db
from app.models.chatbot_context import ChatbotContext
from bson import ObjectId
from pymongo import ReturnDocument

class ChatbotContextRepository:

    @staticmethod
    async def get(user_id: ObjectId) -> ChatbotContext:
        data = await db.chatbot_context.find_one({"user_id": user_id})
        if data:
            return ChatbotContext(**data)
        
        context = ChatbotContext(user_id = user_id)
        await db.chatbot_context.insert_one(context.model_dump( by_alias = True))
        return context

    @staticmethod
    async def update(context: ChatbotContext) -> ChatbotContext:
        data = await db.chatbot_context.find_one_and_update(
            {"user_id": context.user_id}, 
            {"$set": context.model_dump(by_alias = True)},
            return_document = ReturnDocument.AFTER 
        ) 
        return ChatbotContext(**data)
    
    @staticmethod
    async def reset(user_id: ObjectId):
        await db.chatbot_context.delete_one({"user_id": user_id})