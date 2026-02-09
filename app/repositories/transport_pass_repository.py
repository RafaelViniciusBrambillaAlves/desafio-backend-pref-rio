from app.core.database import db
from app.models.transport_pass import TransportPass
from bson import ObjectId
from pymongo import ReturnDocument

class TransportPassRepository:

    @staticmethod
    async def get_by_user_id(user_id: ObjectId) -> TransportPass | None:
        data = await db.transport_pass.find_one({"user_id": user_id})
        return TransportPass(**data) if data else None

    @staticmethod
    async def create(user_id: ObjectId) -> TransportPass:
        transport_pass = TransportPass(user_id = user_id)
        result = await db.transport_pass.insert_one(
            transport_pass.model_dump(by_alias = True)
        )
        transport_pass.id = result.inserted_id
        return transport_pass
    
    @staticmethod
    async def update_balance(user_id: ObjectId, amount: float) -> TransportPass:
        data = await db.transport_pass.find_one_and_update(
            {"user_id": user_id},
            {"$inc": {"balance": amount}},
            return_document = True
        )
        return TransportPass(**data)
    
    @staticmethod 
    async def debit_balance(user_id: ObjectId, amount: float) -> TransportPass | None:
        data = await db.transport_pass.find_one_and_update(
            {
                "user_id": user_id,
                "balance": {"$gte": amount}
            },
            {
                "$inc": {"balance": -amount}
            },
            return_document = ReturnDocument.AFTER
        )

        return TransportPass(**data) if data else None
    
