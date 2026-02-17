from fastapi import Depends
from app.dependencies.user_dependencies import get_user_repository
from app.application.use_cases.auth.login_user_use_case import LoginUserUseCase
from app.application.use_cases.auth.refresh_token_use_case import RefreshTokenUseCase
from app.application.use_cases.auth.login_with_google_use_case import LoginWithGoogleUseCase



def get_login_use_case(repository = Depends(get_user_repository)):
    return LoginUserUseCase(repository)

def get_refresh_token_use_case(repository = Depends(get_user_repository)):
    return RefreshTokenUseCase(repository)

def get_google_login_use_case(repository = Depends(get_user_repository)):
    return LoginWithGoogleUseCase(repository)
