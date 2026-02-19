from fastapi import status
from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.schemas.auth import TokenResponse
from app.core.jwt import JWTService
from app.core.exceptions import AppException
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork


class RefreshTokenUseCase:

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def execute(self, refresh_token: str) -> TokenResponse:
        
        payload = JWTService.decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise AppException(
                error = "INVALID_TOKEN_TYPE",
                message = "Invalid token type",
                status_code = status.HTTP_401_UNAUTHORIZED  
            )

        async with self._uow:

            user = await self._uow.users.get_by_id(payload.get("sub"))

            if not user:
                raise AppException(
                    error = "USER_NOT_FOUND",
                    message = "User not found",
                    status_code = status.HTTP_401_UNAUTHORIZED 
                )
            
        return TokenResponse(
            access_token = JWTService.create_access_token(user.id),
            refresh_token = refresh_token
        )