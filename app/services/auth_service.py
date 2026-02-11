from fastapi import status
from app.schemas.auth import LoginResponse, TokenResponse
from app.core.security import Security
from app.core.exceptions import AppException
from app.schemas.user import UserPublic 
from app.core.jwt import JWTService
import httpx
from app.core.config import settings
from app.models.user import User
from app.repositories.interfaces.user_repository_interface import IUserRepository 

class AuthService:

    def __init__(self, repository: IUserRepository):
       self.repository = repository


    async def login(self, email: str, password: str) -> LoginResponse:
        user = await self.repository.get_by_email(email)

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

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        payload = JWTService.decode_token(refresh_token)
       
        if payload.get("type") != "refresh":
            raise AppException(
                error = "INVALID_TOKEN_TYPE",
                message = "User not found.",
                status_code = status.HTTP_401_UNAUTHORIZED
            )
        
        user = await self.repository.get_by_id(payload.get("sub"))

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
    
    async def login_with_google(self, code: str) -> LoginResponse:
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(
                "https://oauth2.googleapis.com/token",
                data = {
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI 
                }
            )

        token_data = token_resp.json()
        if "access_token" not in token_data:
            raise AppException(
                error = "",
                message = "",
                status_code = status.HTTP_401_UNAUTHORIZED 
            )

        access_token = token_data["access_token"]

        async with httpx.AsyncClient() as client:
            userinfo = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers = {"Authorization": f"Bearer {access_token}"}
            )
        
        google_user = userinfo.json()

        user = await self.repository.get_by_email(google_user["email"])

        if not user:
            user = User(
                email= google_user["email"],
                password = None,
                provider = "google" 
            )
            user = await self.repository.create(user)

        return LoginResponse(
            user = {
                "id": str(user.id),
                "email": user.email
            },
            tokens = TokenResponse(
                access_token = JWTService.create_access_token(user.id),
                refresh_token = JWTService.create_refresh_token(user.id)
            )
        )
    