from fastapi import APIRouter, Depends, status
from app.schemas.response import SucessResponse
from app.schemas.auth import LoginResponse, LoginRequest, RefreshTokenRequest
# from app.services.auth_service import AuthService
from fastapi.responses import RedirectResponse 
from app.core.oauth.google import google_oauth
from app.application.use_cases.auth.login_user_use_case import LoginUserUseCase
from app.dependencies.auth_dependencies import get_login_use_case
from app.application.use_cases.auth.refresh_token_use_case import RefreshTokenUseCase
from app.dependencies.auth_dependencies import get_refresh_token_use_case
from app.application.use_cases.auth.login_with_google_use_case import LoginWithGoogleUseCase
from app.dependencies.auth_dependencies import get_google_login_use_case

router = APIRouter(prefix = "/auth", tags = ["auth"])

@router.post(
    "/login",
    response_model = SucessResponse[LoginResponse],
    summary = "Login using JSON payload" 
)
async def login_json(
    data: LoginRequest,
    use_case: LoginUserUseCase = Depends(get_login_use_case)
):
    result = await use_case.execute(data.email, data.password)

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
    use_case: RefreshTokenUseCase = Depends(get_refresh_token_use_case)
):
    tokens = await use_case.execute(data.refresh_token)

    return SucessResponse(
        message = "Token refreshed successfully", 
        data = tokens
    )

@router.get(
    "/google/login",
    status_code = status.HTTP_200_OK,
    summary = "Login with Google",
    description = """
        http://localhost:8000/auth/google/login
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
    use_case: LoginWithGoogleUseCase = Depends(get_google_login_use_case)
):
    result = await use_case.execute(code)

    return SucessResponse(
        message = "Login with Google successfully",
        data = result
    )