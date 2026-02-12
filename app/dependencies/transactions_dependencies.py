from fastapi import Depends
from app.dependencies.database_dependencies import get_database
from app.repositories.transaction_repositoy import TransactionRepository
from app.services.transactions_service import TransactionService

def get_transaction_repository(db = Depends(get_database)):
    return TransactionRepository(db)

def get_transaction(repository = Depends(get_transaction_repository)):
    return TransactionService(repository)