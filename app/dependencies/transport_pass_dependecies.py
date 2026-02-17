from fastapi import Depends
from app.dependencies.database_dependencies import get_database
from app.repositories.transport_pass_repository import TransportPassRepository
from app.repositories.transaction_repositoy import TransactionRepository
from app.application.use_cases.transport_pass.get_balance_use_case import GetBalanceUseCase
from app.application.use_cases.transport_pass.recharge_transport_pass_use_case import RechargeTransportPassUseCase
from app.application.use_cases.transport_pass.use_transport_pass_use_case import UseTransportPassUseCase


def get_transport_pass_repository(db=Depends(get_database)):
    return TransportPassRepository(db)


def get_transaction_repository(db=Depends(get_database)):
    return TransactionRepository(db)


def get_balance_use_case(
    transport_repo = Depends(get_transport_pass_repository)
):
    return GetBalanceUseCase(transport_repo)


def get_recharge_use_case(
    transport_repo = Depends(get_transport_pass_repository),
    transaction_repo  =Depends(get_transaction_repository)
):
    return RechargeTransportPassUseCase(transport_repo, transaction_repo)


def get_use_transport_use_case(
    transport_repo = Depends(get_transport_pass_repository),
    transaction_repo = Depends(get_transaction_repository)
):
    return UseTransportPassUseCase(transport_repo, transaction_repo)
