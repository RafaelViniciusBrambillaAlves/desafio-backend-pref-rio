from fastapi import Depends
from app.repositories.user_repository import MongoUserRepository
from app.dependencies.database_dependencies import get_database

from app.application.use_cases.user.create_user_use_case import CreateUserUseCase
from app.application.use_cases.user.get_user_use_case import GetUserUseCase
from app.application.use_cases.user.delete_user_use_case import DeleteUserUseCase


def get_user_repository(db = Depends(get_database)):
    return MongoUserRepository(db)

def get_create_user_use_case(repository = Depends(get_user_repository)):
    return CreateUserUseCase(repository)

def get_get_user_use_case(repository = Depends(get_user_repository)):
    return GetUserUseCase(repository)

def get_delete_user_use_case(repository = Depends(get_user_repository)):
    return DeleteUserUseCase(repository)
