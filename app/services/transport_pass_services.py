from fastapi import status
from bson import ObjectId
from app.repositories.transport_pass_repository import TransportPassRepository
from app.core.exceptions import AppException
from app.repositories.transaction_repositoy import TransactionRepository
from app.domain.transaction_type import TransactionType
from app.models.transaction import Transaction


class TransportPassService:

    @classmethod
    async def get_or_create(cls, user_id: ObjectId):
        transport_pass = await TransportPassRepository.get_by_user_id(user_id)
        if not transport_pass:
            transport_pass = await TransportPassRepository.create(user_id)
        return transport_pass
    
    @classmethod
    async def get_balance(cls, user_id: ObjectId) -> float: 
        transport_pass = await cls.get_or_create(user_id)
        return transport_pass.balance

    @classmethod
    async def recharge(cls, user_id: ObjectId, amount: float) -> float:
        if amount <= 0:
            raise AppException(
                error = "INVALID_AMOUNT",
                message = "Recharge amount must be greater than zero",
                status_code = status.HTTP_400_BAD_REQUEST
            )
        
        transport_pass = await TransportPassRepository.get_by_user_id(user_id)

        balance_before = transport_pass.balance

        updated_pass = await TransportPassRepository.update_balance(
            user_id = user_id, 
            amount = amount
        )

        transaction =  Transaction(
            user_id = user_id,
            type = TransactionType.RECHARGE,
            amount = amount,
            balance_before = balance_before,
            balance_after = updated_pass.balance
        )

        await TransactionRepository.create(transaction)

        return updated_pass.balance

    @classmethod
    async def use(cls, user_id: ObjectId, amount: float) -> float:
        if amount <= 0:
            raise AppException(
                error = "INVALID_AMOUNT",
                message = "Amount must be greater than zero",
                status_code = status.HTTP_400_BAD_REQUEST
            )
        
        transport_pass = await TransportPassRepository.get_by_user_id(user_id)

        if transport_pass.balance < amount:
            raise AppException(
                error = "INSUFFICIENT_BALANCE",
                message = "Insufficient balance to complete this operation.",
                status_code = status.HTTP_409_CONFLICT
            )
        balance_before = transport_pass.balance

        update_pass = await TransportPassRepository.debit_balance(
            user_id = user_id,
            amount = amount
        )

        transaction = Transaction(
            user_id = user_id,
            type = TransactionType.USE,
            amount = amount,
            balance_before = balance_before,
            balance_after = update_pass.balance
        )
        await TransactionRepository.create(transaction)

        return update_pass.balance