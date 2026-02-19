from app.models.document import Document
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.client_session import ClientSession
from app.repositories.base_repository import BaseMongoRepository

class DocumentMetadataRepository(BaseMongoRepository):

    def __init__(self, database: AsyncIOMotorDatabase):
        super().__init__(database)

    async def create(self, document: Document) -> Document:
        result = await self._db.documents.insert_one(
            document.model_dump(by_alias = True, exclude_none = True),
            session = self._session
        )
        document.id = result.inserted_id
        return document
    
    async def list_by_user(self, user_id: ObjectId):
        cursor = self._db.documents.find({"user_id": user_id}, session = self._session)
        return [Document(**doc) async for doc in cursor]