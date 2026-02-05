from fastapi import status, UploadFile
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.exceptions import AppException
from app.core.security import Security
from app.services.documents_services import DocumentService

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

        user = await UserRepository.get_by_id(id)

        if not user:
            raise AppException(
                error = "USER_NOT_FOUND",
                message = "User not found",
                status_code = status.HTTP_404_NOT_FOUND
            )

        return user
    
    @classmethod
    async def delete_user(cls, id: str) -> User:
        user = await UserRepository.delete_by_id(id)

        if not user:
            raise AppException(
                error = "USER_NOT_FOUND",
                message = "User not found.",
                status_code = status.HTTP_404_NOT_FOUND
            )
        return user

    @staticmethod
    async def upload_documents(user: User, file: UploadFile) -> str:
        return await DocumentService.upload(
            user_id = user.id, 
            file = file
        )