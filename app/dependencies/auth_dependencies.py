from app.services.auth_service import AuthService
from app.repositories.user_repository import MongoUserRepository
from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.dependencies.user_dependencies import get_user_repository
from fastapi import Depends

def get_auth_service(repository: IUserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repository)