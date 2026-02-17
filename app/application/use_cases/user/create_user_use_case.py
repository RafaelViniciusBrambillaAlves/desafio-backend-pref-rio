from fastapi import status
from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.exceptions import AppException
from app.core.security import Security

class CreateUserUseCase:

    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def execute(self, user_data: UserCreate) -> User:
        await self._validate_email(user_data.email)

        hashed_password = Security.hash_password(user_data.password)

        user = User(
            email = user_data.email,
            password = hashed_password 
        )

        return await self._repository.create(user)

    async def _validate_email(self, email: str) -> None:
        if await self._repository.get_by_email(email):
            raise AppException(
                error = "EMAIL_ALREADY_EXISTS",
                message = "A user with this email already exits.",
                status_code = status.HTTP_409_CONFLICT
            )