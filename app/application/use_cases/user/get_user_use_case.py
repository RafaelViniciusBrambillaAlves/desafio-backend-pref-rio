from fastapi import status
# from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.models.user import User
from app.core.exceptions import AppException
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork

class GetUserUseCase:

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def execute(self, user_id: str) -> User:
        
        async with self._uow:

            user = await self._uow.users.get_by_id(user_id)

            if not user:
                raise AppException(
                    error = "USER_NOT_FOUND",
                    message = "User not found",
                    status_code = status.HTTP_404_NOT_FOUND
                )
            return user