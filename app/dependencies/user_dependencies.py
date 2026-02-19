from fastapi import Depends
from app.application.use_cases.user.create_user_use_case import CreateUserUseCase
from app.application.use_cases.user.get_user_use_case import GetUserUseCase
from app.application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from app.repositories.unit_of_work.mongo_unit_of_work import MongoUnitOfWork
from app.repositories.interfaces.unit_of_work_interface  import IUnitOfWork
from app.dependencies.database_dependencies import get_unit_of_work



def get_create_user_use_case(uow: IUnitOfWork = Depends(get_unit_of_work)):
    return CreateUserUseCase(uow)

def get_get_user_use_case(uow: IUnitOfWork = Depends(get_unit_of_work)):
    return GetUserUseCase(uow)

def get_delete_user_use_case(uow: IUnitOfWork = Depends(get_unit_of_work)):
    return DeleteUserUseCase(uow)
