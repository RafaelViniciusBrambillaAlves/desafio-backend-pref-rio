from fastapi import status
from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.schemas.auth import TokenResponse, LoginResponse
from app.core.security import Security
from app.core.jwt import JWTService
from app.schemas.user import UserPublic
from app.core.exceptions import AppException
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork

class LoginUserUseCase:

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def execute(self, email: str, password: str) -> LoginResponse:
        async with self._uow:

            user = await self._uow.users.get_by_email(email)

            if not user or not user.password:
                raise self._invalid_credentials()

            if not Security.verify_password(password, user.password):
                raise self._invalid_credentials()

            return self._build_response(user)
        
    def _build_response(self, user) -> LoginResponse:
        tokens = TokenResponse(
            access_token = JWTService.create_access_token(user.id),
            refresh_token = JWTService.create_refresh_token(user.id)
        )

        return LoginResponse(
            user = UserPublic(
                id = str(user.id),
                email = user.email
            ),
            tokens = tokens
        )

    def _invalid_credentials(self):
        return AppException(
            error = "INVALID_CREDENTIALS",
            message = "Email or password is incorrect",
            status_code = status.HTTP_401_UNAUTHORIZED
        )