from app.models.user import User
from bson import ObjectId
from bson.errors import InvalidId
from app.repositories.interfaces.user_repository_interface import IUserRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.client_session import ClientSession
from app.repositories.base_repository import BaseMongoRepository
class MongoUserRepository(BaseMongoRepository, IUserRepository):
    
    def __init__(self, database: AsyncIOMotorDatabase):
        super().__init__(database)
    
    
    async def create(self, user: User) -> User:
        result = await self._db.user.insert_one(
            user.model_dump(by_alias = True, exclude_none=True),
            session = self._session
        )
        user.id = result.inserted_id
        return user
  
    async def get_by_email(self, email: str) -> User | None:
        data = await self._db.user.find_one(
            {"email": email},
            session = self._session
        )
        return User(**data) if data else None
    
    async def get_by_id(self, id: str) -> User | None:
        try:
            object_id = ObjectId(id)
        except InvalidId:
            return None

        data = await self._db.user.find_one(
            {"_id": object_id},
            session = self._session
        )
        return User(**data) if data else None

    async def delete_by_id(self, id: str) -> User | None:
        try:
            object_id = ObjectId(id)
        except InvalidId:
            return None

        data = await self._db.user.find_one_and_delete(
            {"_id": object_id},
            session = self._session
        )
        return User(**data) if data else None
