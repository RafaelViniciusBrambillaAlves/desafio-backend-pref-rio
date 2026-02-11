from app.services.auth_service import AuthService
from app.repositories.user_repository import MongoUserRepository
from app.repositories.interfaces.user_repository_interface import IUserRepository

def get_auth_service() -> AuthService:
    repository: IUserRepository = MongoUserRepository()
    return AuthService(repository)