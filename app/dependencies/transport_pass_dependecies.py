from fastapi import Depends
from app.application.use_cases.transport_pass.get_balance_use_case import GetBalanceUseCase
from app.application.use_cases.transport_pass.recharge_transport_pass_use_case import RechargeTransportPassUseCase
from app.application.use_cases.transport_pass.use_transport_pass_use_case import UseTransportPassUseCase
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork
from app.repositories.unit_of_work.mongo_unit_of_work import MongoUnitOfWork
from app.dependencies.database_dependencies import get_unit_of_work

def get_balance_use_case(
    uow: IUnitOfWork = Depends(get_unit_of_work)
):
    return GetBalanceUseCase(uow)


def get_recharge_use_case(
    # uow: IUnitOfWork = Depends(get_unit_of_work)
):
    # return RechargeTransportPassUseCase(uow)
    return RechargeTransportPassUseCase()


def get_use_transport_use_case(
    uow: IUnitOfWork = Depends(get_unit_of_work)
):
    return UseTransportPassUseCase(uow)
