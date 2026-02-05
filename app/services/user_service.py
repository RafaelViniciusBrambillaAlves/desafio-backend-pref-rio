from fastapi import status
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.exceptions import AppException
from app.core.security import Security
from bson import ObjectId

class UserService:

    @staticmethod
    async def _validate_email(email: str):
        if await UserRepository.get_by_email(email):
            raise AppException(
                error = "EMAIL_ALREADY_EXISTS",
                message = "A user with this email already exists.",
                status_code = status.HTTP_409_CONFLICT
            )

    @classmethod
    async def register(cls, user: UserCreate) -> User:
        await cls._validate_email(user.email)

        user.password = Security.hash_password(user.password)

        user_model = User(**user.model_dump())
        return await UserRepository.create(user_model)

    @classmethod
    async def list_user(cls, id: str) -> User:
        try:
            object_id = ObjectId(id)
        except:
            raise AppException(
                error = "INVALID_ID",
                message = "The id is not valid",
                status_code = status.HTTP_400_BAD_REQUEST
            ) 

        user = await UserRepository.get_by_id(id)

        if not user:
            raise AppException(
                error = "USER_NOT_FOUND",
                message = "User not found",
                status_code = status.HTTP_404_NOT_FOUND
            )

        return user