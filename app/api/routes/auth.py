from fastapi import APIRouter
from app.schemas.response import SucessResponse
from app.schemas.auth import LoginResponse, LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix = "/auth", tags = ["auth"])

@router.post(
    "/login/json",
    response_model = SucessResponse[LoginResponse],
    summary = "Login using JSON payload" 
)
async def login_json(data: LoginRequest):
    login_response = await AuthService.login(data.email, data.password)

    return SucessResponse(
        message = "Login successful.",
        data = login_response
    )