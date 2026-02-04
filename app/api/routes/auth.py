from fastapi import APIRouter, Depends, status
from app.schemas.response import SucessResponse
from app.schemas.auth import LoginResponse, LoginRequest, RefreshTokenRequest
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse 
from app.core.oauth.google import google_oauth

router = APIRouter(prefix = "/auth", tags = ["auth"])

# @router.post(
#     "/login",
#     summary = "Login with OAuth2"
# )
# async def login_oauth2(form_data: OAuth2PasswordRequestForm = Depends()):
#     result = await AuthService.login(form_data.username, form_data.password)

#     return {
#         "access_token": result.tokens.access_token,
#         "token_type": "bearer"
#     }

@router.post(
    # "/login/json",
    "/login",
    response_model = SucessResponse[LoginResponse],
    summary = "Login using JSON payload" 
)
async def login_json(data: LoginRequest):
    login_response = await AuthService.login(data.email, data.password)

    return SucessResponse(
        message = "Login successful.",
        data = login_response
    )

@router.post(
    "/refresh",
    status_code = status.HTTP_200_OK,
    summary = "Refresh access token"
)
async def refresh_token(data: RefreshTokenRequest):
    return await AuthService.refresh_token(data.refresh_token)

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
async def google_callback(code: str):
    return await AuthService.login_with_google(code)