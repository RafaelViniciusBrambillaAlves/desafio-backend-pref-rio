from fastapi import Depends
from app.repositories.user_repository import MongoUserRepository
from app.services.user_service import UserService
from app.dependencies.database_dependencies import get_database

def get_user_repository(db = Depends(get_database)):
    return MongoUserRepository(db)

def get_user_service(repository = Depends(get_user_repository)):
    return UserService(repository)