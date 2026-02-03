from fastapi import status
from app.schemas.auth import LoginResponse
from app.repositories.user_repository import UserRepository
from app.core.security import Security
from app.core.exceptions import AppException
from app.schemas.user import UserPublic

class AuthService:

    @staticmethod
    async def login(email: str, password: str) -> LoginResponse:
        user = await UserRepository.get_by_email(email)

        if not user and not Security.verify_password(password, user.password):
            raise AppException(
                error = "INVALID_CREDENTIALS",
                message = "Email or password is incorrect.",
                status_code = status.HTTP_401_UNAUTHORIZED  
            )

        return LoginResponse(
            user = UserPublic (
                id = str(user.id),
                email = user.email
            )
        )