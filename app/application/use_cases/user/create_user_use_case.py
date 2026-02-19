from fastapi import status
# from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.exceptions import AppException
from app.core.security import Security
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork

class CreateUserUseCase:

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def execute(self, user_data: UserCreate) -> User:
        async with self._uow: 

            await self._validate_email(user_data.email)

            hashed_password = Security.hash_password(user_data.password)

            user = User(
                email = user_data.email,
                password = hashed_password 
            )

            return await self._uow.users.create(user)

    async def _validate_email(self, email: str) -> None:
        if await self._uow.users.get_by_email(email):
            raise AppException(
                error = "EMAIL_ALREADY_EXISTS",
                message = "A user with this email already exits.",
                status_code = status.HTTP_409_CONFLICT
            )