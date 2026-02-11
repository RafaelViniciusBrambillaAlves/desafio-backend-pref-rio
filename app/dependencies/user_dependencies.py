from app.repositories.user_repository import MongoUserRepository
from app.services.user_service import UserService

def get_user_service() -> UserService:
    repository = MongoUserRepository()
    return UserService(repository)