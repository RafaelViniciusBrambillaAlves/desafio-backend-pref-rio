from fastapi import status
from app.schemas.auth import LoginResponse, TokenResponse
from app.repositories.user_repository import UserRepository
from app.core.security import Security
from app.core.exceptions import AppException
from app.schemas.user import UserPublic 
from app.core.jwt import JWTService

class AuthService:

    @staticmethod
    async def login(email: str, password: str) -> LoginResponse:
        user = await UserRepository.get_by_email(email)

        if not user or not Security.verify_password(password, user.password):
            raise AppException(
                error = "INVALID_CREDENTIALS",
                message = "Email or password is incorrect.",
                status_code = status.HTTP_401_UNAUTHORIZED  
            )

        tokens = TokenResponse(
            access_token = JWTService.create_access_token(user.id),
            refresh_token = JWTService.create_refresh_token(user.id)
        )

        return LoginResponse(
            user = UserPublic (
                id = str(user.id),
                email = user.email
            ),
            tokens = tokens
        )

    @staticmethod
    async def refresh_token(refresh_token: str) -> TokenResponse:
        payload = JWTService.decode_token(refresh_token)
       
        if payload.get("type") != "refresh":
            raise AppException(
                error = "INVALID_TOKEN_TYPE",
                message = "User not found.",
                status_code = status.HTTP_401_UNAUTHORIZED
            )
        
        user = await UserRepository.get_by_id(payload.get("sub"))

        if not user:
            raise AppException(
                error = "USER_NOT_FOUND",
                message = "User not found.", 
                status_code = status.HTTP_401_UNAUTHORIZED
            )

        return TokenResponse(
            access_token = JWTService.create_access_token(user.id),
            refresh_token = refresh_token
        )