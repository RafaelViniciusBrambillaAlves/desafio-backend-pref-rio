from fastapi import Depends
from app.application.use_cases.transaction.list_transactions_use_case import ListTransactionsUseCase
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork
from app.repositories.unit_of_work.mongo_unit_of_work import MongoUnitOfWork
from app.dependencies.database_dependencies import get_unit_of_work


def get_list_transaction_use_case(uow = Depends(get_unit_of_work)):
    return ListTransactionsUseCase(uow)