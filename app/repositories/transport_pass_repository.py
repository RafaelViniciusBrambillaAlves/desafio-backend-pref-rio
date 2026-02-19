from app.models.transport_pass import TransportPass
from bson import ObjectId
from pymongo import ReturnDocument
from app.repositories.base_repository import BaseMongoRepository
from app.repositories.interfaces.transportpass_pass_repository_interface import ITransportPassRepository

class TransportPassRepository(BaseMongoRepository, ITransportPassRepository):

    def __init__(self, database):
        super().__init__(database)

    async def get_by_user_id(self, user_id: ObjectId) -> TransportPass | None:
        data = await self._db.transport_pass.find_one({"user_id": user_id}, session = self._session)
        return TransportPass(**data) if data else None

    async def create(self, user_id: ObjectId) -> TransportPass:
        transport_pass = TransportPass(user_id = user_id)
        result = await self._db.transport_pass.insert_one(
            transport_pass.model_dump(by_alias = True),
            session = self._session
        )
        transport_pass.id = result.inserted_id
        return transport_pass

    async def update_balance(self, user_id: ObjectId, amount: float) -> TransportPass:
        data = await self._db.transport_pass.find_one_and_update(
            {"user_id": user_id},
            {"$inc": {"balance": amount}},
            return_document = ReturnDocument.AFTER,
            session = self._session
        )
        return TransportPass(**data)
     
    async def debit_balance(self, user_id: ObjectId, amount: float) -> TransportPass | None:
        data = await self._db.transport_pass.find_one_and_update(
            {
                "user_id": user_id,
                "balance": {"$gte": amount}
            },
            {
                "$inc": {"balance": -amount}
            },
            return_document = ReturnDocument.AFTER,
            session = self._session
        )

        return TransportPass(**data) if data else None
    
