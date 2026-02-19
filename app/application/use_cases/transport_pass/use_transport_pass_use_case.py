from fastapi import status
from bson import ObjectId
from app.repositories.interfaces.transaction_repository_interface import ITransactionRepository
from app.core.exceptions import AppException
from app.models.transaction import Transaction
from app.domain.transaction_type import TransactionType
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork


class UseTransportPassUseCase:

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def execute(self, user_id: ObjectId, amount: float) -> float:
        if amount <= 0:
            raise AppException(
                error = "INVALID_AMOUNT",
                message = "Amount must be greater than zero", 
                status_code = status.HTTP_400_BAD_REQUEST
            )
        
        async with self._uow:
        
            transport_pass = await self._uow.transport_passes.get_by_user_id(user_id)

            if not transport_pass:
                raise AppException(
                    error = "TRANSPORT_PASS_NOT_FOUND", 
                    message = "Transport pass not found",
                    status_code = status.HTTP_404_NOT_FOUND
                )
            
            if transport_pass.balance < amount:
                raise AppException(
                    error = "INSUFFICIENT_BALANCE", 
                    message = "Insufficient balance to complete this operation",
                    status_code = status.HTTP_409_CONFLICT
                )
            
            balance_before = transport_pass.balance

            updated_pass = await self._uow.transport_passes.debit_balance(
                user_id = user_id, 
                amount = amount
            )

            transaction = Transaction(
                user_id = user_id,
                type = TransactionType.USE,
                amount = amount,
                balance_before = balance_before,
                balance_after = updated_pass.balance 
            )

            await self._uow.transactions.create(transaction)

        return updated_pass.balance