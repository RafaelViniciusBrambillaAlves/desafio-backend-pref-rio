from fastapi import Depends
from app.dependencies.database_dependencies import get_database
from app.repositories.transaction_repositoy import TransactionRepository
from app.application.use_cases.transaction.list_transactions_use_case import ListTransactionsUseCase

def get_transaction_repository(db = Depends(get_database)):
    return TransactionRepository(db)

def get_list_transaction_use_case(repository = Depends(get_transaction_repository)):
    return ListTransactionsUseCase(repository)