from fastapi import APIRouter, Depends, status
from app.core.auth_dependencies import get_current_user
from app.models.user import User
from app.schemas.response import SucessResponse
from app.schemas.transport_pass import BalanceResponse, RechargeRequest, DebitRequest
# from app.services.transport_pass_services import TransportPassService
# from app.dependencies.transport_pass_dependecies import get_transport_pass_service

from app.dependencies.user_dependencies import get_create_user_use_case
from app.application.use_cases.user.create_user_use_case import CreateUserUseCase

from app.dependencies.transport_pass_dependecies import get_balance_use_case
from app.application.use_cases.transport_pass.get_balance_use_case import GetBalanceUseCase
from app.dependencies.transport_pass_dependecies import get_recharge_use_case
from app.application.use_cases.transport_pass.recharge_transport_pass_use_case import RechargeTransportPassUseCase
from app.dependencies.transport_pass_dependecies import get_use_transport_use_case
from app.application.use_cases.transport_pass.use_transport_pass_use_case import UseTransportPassUseCase 
from app.dependencies.database_dependencies import get_unit_of_work
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork

router = APIRouter(prefix = "/transport-pass", tags = ["Transport Pass"])

@router.get(
    "/balance",
    status_code = status.HTTP_200_OK,
    response_model = SucessResponse[BalanceResponse]
)
async def get_balance(
    current_user: User = Depends(get_current_user),
    service: GetBalanceUseCase = Depends(get_balance_use_case)
):
    balance = await service.execute(current_user.id)

    return SucessResponse(
        message = "Balance retrieved successfully.",
        data = BalanceResponse(balance = balance)
    )

@router.post(
    "/recharge",
    status_code = status.HTTP_200_OK,
    response_model = SucessResponse[BalanceResponse]
)
async def recharge(
    payload: RechargeRequest, 
    current_user: User = Depends(get_current_user),
    uow: IUnitOfWork = Depends(get_unit_of_work),
    service: RechargeTransportPassUseCase = Depends(get_recharge_use_case)
):
    async with uow:

        balance = await service.execute(
            uow,
            current_user.id,
            payload.amount
        )

    return SucessResponse(
        message = "Recharge successful",
        data = BalanceResponse(balance = balance)
    )

@router.post(
    "/use",
    status_code = status.HTTP_200_OK,
    response_model = SucessResponse[BalanceResponse]
)
async def use_transport(
    payload: DebitRequest, 
    current_user: User = Depends(get_current_user),
    service: UseTransportPassUseCase = Depends(get_use_transport_use_case)
):
    balance = await service.execute(
        current_user.id,
        payload.amount
    )

    return SucessResponse(
        message = "Balance debited successfully",
        data = BalanceResponse(balance = balance)
    )