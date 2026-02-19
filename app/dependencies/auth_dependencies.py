from fastapi import Depends
from app.application.use_cases.auth.login_user_use_case import LoginUserUseCase
from app.application.use_cases.auth.refresh_token_use_case import RefreshTokenUseCase
from app.application.use_cases.auth.login_with_google_use_case import LoginWithGoogleUseCase
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork
from app.dependencies.database_dependencies import get_unit_of_work

def get_login_use_case(
    uow: IUnitOfWork = Depends(get_unit_of_work)
):
    return LoginUserUseCase(uow)

def get_refresh_token_use_case(
    uow: IUnitOfWork = Depends(get_unit_of_work)
):
    return RefreshTokenUseCase(uow)

def get_google_login_use_case(
    uow: IUnitOfWork = Depends(get_unit_of_work)
):
    return LoginWithGoogleUseCase(uow)
