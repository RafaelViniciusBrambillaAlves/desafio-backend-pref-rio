from app.core.database import db
from app.models.user import User
from bson import ObjectId
from bson.errors import InvalidId
from app.repositories.interfaces.user_repository_interface import IUserRepository



class MongoUserRepository(IUserRepository):
    
    async def create(self, user: User) -> User:
        result = await db.user.insert_one(user.model_dump(by_alias = True))
        user.id = result.inserted_id
        return user
  
    async def get_by_email(self, email: str) -> User | None:
        data = await db.user.find_one({"email": email})
        return User(**data) if data else None
    
    async def get_by_id(self, id: str) -> User | None:
        try:
            object_id = ObjectId(id)
        except InvalidId:
            return None

        data = await db.user.find_one({"_id": object_id})
        return User(**data) if data else None

    async def delete_by_id(self, id: str) -> User | None:
        try:
            object_id = ObjectId(id)
        except InvalidId:
            return None

        data = await db.user.find_one_and_delete({"_id": object_id})
        return User(**data) if data else None
