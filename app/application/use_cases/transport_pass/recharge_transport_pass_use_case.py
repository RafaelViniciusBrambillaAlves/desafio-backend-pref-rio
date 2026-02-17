from fastapi import status
from app.repositories.interfaces.transportpass_pass_repository_interface import ITransportPassRepository
from app.repositories.interfaces.transaction_repository_interface import ITransactionRepository
from bson import ObjectId
from app.core.exceptions import AppException 
from app.models.transaction import Transaction
from datetime import datetime
from app.domain.transaction_type import TransactionType





class RechargeTransportPassUseCase:

    def __init__(self, transport_repository: ITransportPassRepository, transaction_repository: ITransactionRepository):
        self._transport_repository = transport_repository
        self._transaction_repository = transaction_repository

    async def execute(self, user_id: ObjectId, amount: float) -> float:

        if amount <= 0:
            raise AppException(
                error = "INVALID_AMOUNT",
                message = "Recharge amount must be than zero", 
                status_code = status.HTTP_400_BAD_REQUEST
            )
        
        transport_pass = await self._transport_repository.get_by_user_id(user_id)

        if not transport_pass:
            transport_pass = await self._transport_repository.create(user_id) 

        balance_before = transport_pass.balance

        updated_pass = await self._transport_repository.update_balance(
            user_id = user_id, 
            amount = amount
        )

        transaction = Transaction(
            user_id = user_id,
            type = TransactionType.RECHARGE,
            amount = amount,
            balance_before = balance_before,
            balance_after = updated_pass.balance
        )

        await self._transaction_repository.create(transaction)

        return updated_pass.balance