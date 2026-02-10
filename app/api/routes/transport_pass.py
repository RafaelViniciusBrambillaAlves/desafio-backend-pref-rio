from fastapi import APIRouter, Depends, status
from app.core.auth_dependencies import get_current_user
from app.models.user import User
from app.schemas.response import SucessResponse
from app.schemas.transport_pass import BalanceResponse, RechargeRequest, DebitRequest
from app.services.transport_pass_services import TransportPassService


router = APIRouter(prefix = "/transport-pass", tags = ["Transport Pass"])

@router.get(
    "/balance",
    status_code = status.HTTP_200_OK,
    response_model = SucessResponse[BalanceResponse]
)
async def get_balance(current_user: User = Depends(get_current_user)):
    balance = await TransportPassService.get_balance(current_user.id)

    return SucessResponse(
        message = "Balance retrieved successfully.",
        data = BalanceResponse(balance = balance)
    )

@router.post(
    "/recharge",
    status_code = status.HTTP_200_OK,
    response_model = SucessResponse[BalanceResponse]
)
async def recharge(payload: RechargeRequest, current_user: User = Depends(get_current_user)):
    balance = await TransportPassService.recharge(
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
async def use_transport(payload: DebitRequest, current_user: User = Depends(get_current_user)):
    balance = await TransportPassService.use(
        current_user.id,
        payload.amount
    )

    return SucessResponse(
        message = "Balance debited successfully",
        data = BalanceResponse(balance = balance)
    )