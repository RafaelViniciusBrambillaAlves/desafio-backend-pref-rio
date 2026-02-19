import httpx
from fastapi import status
from app.schemas.auth import LoginResponse, TokenResponse
from app.core.config import settings
from app.core.exceptions import AppException
from app.models.user import User
from app.schemas.user import UserPublic
from app.core.jwt import JWTService
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork

class LoginWithGoogleUseCase:

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow


    async def execute(self, code: str) -> LoginResponse:
        token_data = await self._exchange_code_for_token(code)
        google_user = await self._get_user_info(token_data["access_token"])

        async with self._uow:

            user = await self._uow.users.get_by_email(
                google_user["email"]
            )

            if not user:
                user = User(
                    email = google_user["email"],
                    password = None,
                    provider = "google"
                )
                user = await self._uow.users.create(user)
        
        return self._build_response(user)
    
    def _build_response(self, user) -> LoginResponse:
        return LoginResponse(
            user = UserPublic(
                id = str(user.id),
                email = user.email
            ),
            tokens = TokenResponse(
                access_token = JWTService.create_access_token(user.id),
                refresh_token = JWTService.create_refresh_token(user.id)
            )
        )


    async def _exchange_code_for_token(self, code: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data = {
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI
                }
            )

        if response.status_code != 200:
            raise AppException(
                error = "GOOGLE_AUTH_FAILED",
                message = "Google authentication failed", 
                status_code = status.HTTP_401_UNAUTHORIZED
            )
        
        return response.json()
    
    async def _get_user_info(self, access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )

        if response.status_code != 200:
            raise AppException(
                error = "GOOGLE_USER_INFO_FAILED",
                message = "Failed to fetch Google user info",
                status_code = status.HTTP_401_UNAUTHORIZED
            )

        return response.json()