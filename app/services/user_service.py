from fastapi import status, UploadFile
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.exceptions import AppException
from app.core.security import Security
from app.services.documents_services import DocumentService
from app.repositories.interfaces.user_repository_interface import IUserRepository

class UserService:

    def __init__(self, repository: IUserRepository):
        self.repository = repository


    async def _validate_email(self, email: str):
        if await self.repository.get_by_email(email):
            raise AppException(
                error = "EMAIL_ALREADY_EXISTS",
                message = "A user with this email already exists.",
                status_code = status.HTTP_409_CONFLICT
            )
    

    async def register(self, user_data: UserCreate) -> User:
        await cls._validate_email(user_data.email)

        hashed_password = Security.hash_password(user_data.password)

        user = User(
            email = user_data.email,
            password = hashed_password
        )

        return await self.repository.create(user)


    async def get_user(self, user_id: str) -> User:

        user = await self.repository.get_by_id(user_id)

        if not user:
            raise AppException(
                error = "USER_NOT_FOUND",
                message = "User not found",
                status_code = status.HTTP_404_NOT_FOUND
            )

        return user
    
   
    async def delete_user(self, user_id: str) -> User:
        user = await self.repository.delete_by_id(user_id)

        if not user:
            raise AppException(
                error = "USER_NOT_FOUND",
                message = "User not found.",
                status_code = status.HTTP_404_NOT_FOUND
            )
        return user

    async def upload_documents(user: User, file: UploadFile) -> str:
        return await DocumentService.upload(
            user_id = user.id, 
            file = file
        )
    
    async def list_documents(user: User) -> list[str]:
        return await DocumentService.list_user_documents(user.id)
    
     