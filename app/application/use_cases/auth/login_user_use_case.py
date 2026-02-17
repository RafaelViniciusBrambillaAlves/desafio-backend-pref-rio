from fastapi import status
from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.schemas.auth import TokenResponse, LoginResponse
from app.core.security import Security
from app.core.jwt import JWTService
from app.schemas.user import UserPublic
from app.core.exceptions import AppException

class LoginUserUseCase:

    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def execute(self, email: str, password: str) -> LoginResponse:
        user = await self._repository.get_by_email(email)

        if not user or not user.password:
            raise self._invalid_credentials()

        if not Security.verify_password(password, user.password):
            raise self._invalid_credentials()

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