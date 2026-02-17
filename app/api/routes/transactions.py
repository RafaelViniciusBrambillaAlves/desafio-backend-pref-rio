from fastapi import APIRouter, Depends, status
from app.core.auth_dependencies import get_current_user
from app.models.user import User
from app.schemas.response import SucessResponse
from app.schemas.transaction import TransactionResponse
from app.application.use_cases.transaction.list_transactions_use_case import ListTransactionsUseCase
from app.dependencies.transactions_dependencies import get_list_transaction_use_case


router = APIRouter( prefix = "/transactions", tags = ["Transactions"])

@router.get(
    "/",
    status_code = status.HTTP_200_OK,
    response_model = SucessResponse[list[TransactionResponse]]
)
async def get_transactions(
    current_user: User = Depends(get_current_user),
    use_caes: ListTransactionsUseCase = Depends(get_list_transaction_use_case)
):
    transactions = await use_caes.execute(current_user.id)

    return SucessResponse(
        message = "Transactions retrieved successfully",
        data = transactions
    )