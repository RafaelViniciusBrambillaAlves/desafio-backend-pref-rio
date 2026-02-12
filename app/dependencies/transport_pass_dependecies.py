from fastapi import Depends
from app.dependencies.database_dependencies import get_database
from app.repositories.transaction_repositoy import TransactionRepository
from app.services.transport_pass_services import TransportPassService
from app.repositories.transport_pass_repository import TransportPassRepository


def get_transport_pass_repository(db = Depends(get_database)):
    return TransactionRepository(db)

def get_transport_pass_service(db = Depends(get_database)):
    transport_repo = TransportPassRepository(db)
    transaction_repo = TransactionRepository(db)

    return TransportPassService(
        transport_repository = transport_repo,
        transaction_repository = transaction_repo
    )