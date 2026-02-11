from fastapi import APIRouter, Depends, status
from app.schemas.response import SucessResponse
from app.schemas.auth import LoginResponse, LoginRequest, RefreshTokenRequest
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse 
from app.core.oauth.google import google_oauth
from app.dependencies.auth_dependencies import get_auth_service

router = APIRouter(prefix = "/auth", tags = ["auth"])

@router.post(
    "/login",
    response_model = SucessResponse[LoginResponse],
    summary = "Login using JSON payload" 
)
async def login_json(
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    result = await service.login(data.email, data.password)

    return SucessResponse(
        message = "Login successful.",
        data = result
    )

@router.post(
    "/refresh",
    status_code = status.HTTP_200_OK,
    summary = "Refresh access token"
)
async def refresh_token(
    data: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service)
):
    tokens = await service.refresh_token(data.refresh_token)

    return SucessResponse(
        message = "Token refreshed successfully", 
        data = tokens
    )

@router.get(
    "/google/login",
    status_code = status.HTTP_200_OK,
    summary = "Login with Google",
    description = """
        Link: http://localhost:8000/auth/google/login
    """
)
def google_login():
    auth_url = google_oauth.get_authorization_url()
    return RedirectResponse(auth_url)

@router.get(
    "/google/callback",
    status_code = status.HTTP_200_OK,
    summary = "Callback Google"
)
async def google_callback(
    code: str,
    service: AuthService = Depends(get_auth_service)
):
    result = await service.login_with_google(code)

    return SucessResponse(
        message = "Login with Google successfully",
        data = result
    )