from app.core.database import db
from app.models.user import User
from bson import ObjectId
from bson.errors import InvalidId

class UserRepository:
    
    @staticmethod
    async def create(user: User) -> User:
        result = await db.user.insert_one(user.model_dump(by_alias = True))
        user.id = result.inserted_id
        return user

    @staticmethod
    async def get_by_email(email: str) -> User | None:
        data = await db.user.find_one({"email": email})
        return User(**data) if data else None
    
    @staticmethod
    async def get_by_id(id: str) -> User | None:
        try:
            object_id = ObjectId(id)
        except InvalidId:
            return None

        data = await db.user.find_one({"_id": object_id})
        return User(**data) if data else None

    @staticmethod
    async def delete_by_id(id: str) -> User | None:
        try:
            object_id = ObjectId(id)
        except InvalidId:
            return None

        data = await db.user.find_one_and_delete({"_id": object_id})
        return User(**data) if data else None
