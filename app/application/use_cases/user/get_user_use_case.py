from fastapi import status
from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.models.user import User
from app.core.exceptions import AppException

class GetUserUseCase:

    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def execute(self, user_id: str) -> User:
        user = await self._repository.get_by_id(user_id)

        if not user:
            raise AppException(
                error = "USER_NOT_FOUND",
                message = "User not found",
                status_code = status.HTTP_404_NOT_FOUND
            )

        return user