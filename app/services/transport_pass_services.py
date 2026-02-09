from fastapi import status
from bson import ObjectId
from app.repositories.transport_pass_repository import TransportPassRepository
from app.core.exceptions import AppException


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
        
        await cls.get_or_create(user_id)

        updated_pass = await TransportPassRepository.update_balance(
            user_id,
            amount
        )
        return updated_pass .balance
    
    @classmethod
    async def use_balance(cls, user_id: ObjectId, amount: float) -> float:
        if amount <= 0:
            raise AppException(
                error = "INVALID_AMOUNT",
                message = "Amount must be greater than zero",
                status_code = status.HTTP_400_BAD_REQUEST
            )
        
        update_pass = await TransportPassRepository.debit_balance(
            user_id = user_id,
            amount = amount
        )

        if not update_pass:
            raise AppException(
                error = "INSUFFICIENT_BALANCE",
                message = "Insufficient balance to complete this operation",
                status_code = status.HTTP_409_CONFLICT
            )

        return update_pass.balance