# from fastapi import status
# from bson import ObjectId
# from app.core.exceptions import AppException
# from app.domain.transaction_type import TransactionType
# from app.models.transaction import Transaction
# from app.repositories.interfaces.transportpass_pass_repository_interface import ITransportPassRepository
# from app.repositories.interfaces.transaction_repository_interface import ITransactionRepository


# class TransportPassService:

#     def __init__(self, transport_repository: ITransportPassRepository, transaction_repository: ITransactionRepository):
#         self.transport_repository = transport_repository
#         self.transaction_repository = transaction_repository


#     async def get_or_create(self, user_id: ObjectId):
#         transport_pass = await self.transport_repository.get_by_user_id(user_id)
#         if not transport_pass:
#             transport_pass = await self.transport_repository.create(user_id)
#         return transport_pass


#     async def get_balance(self, user_id: ObjectId) -> float: 
#         transport_pass = await self.get_or_create(user_id)
#         return transport_pass.balance

    
#     async def recharge(self, user_id: ObjectId, amount: float) -> float:
#         if amount <= 0:
#             raise AppException(
#                 error = "INVALID_AMOUNT",
#                 message = "Recharge amount must be greater than zero",
#                 status_code = status.HTTP_400_BAD_REQUEST
#             )
        
#         transport_pass = await self.transport_repository.get_by_user_id(user_id)

#         balance_before = transport_pass.balance

#         updated_pass = await self.transport_repository.update_balance(
#             user_id = user_id, 
#             amount = amount
#         )

#         transaction =  Transaction(
#             user_id = user_id,
#             type = TransactionType.RECHARGE,
#             amount = amount,
#             balance_before = balance_before,
#             balance_after = updated_pass.balance
#         )

#         await self.transaction_repository.create(transaction)

#         return updated_pass.balance


#     async def use(self, user_id: ObjectId, amount: float) -> float:
#         if amount <= 0:
#             raise AppException(
#                 error = "INVALID_AMOUNT",
#                 message = "Amount must be greater than zero",
#                 status_code = status.HTTP_400_BAD_REQUEST
#             )
        
#         transport_pass = await self.transport_repository.get_by_user_id(user_id)

#         if transport_pass.balance < amount:
#             raise AppException(
#                 error = "INSUFFICIENT_BALANCE",
#                 message = "Insufficient balance to complete this operation.",
#                 status_code = status.HTTP_409_CONFLICT
#             )
#         balance_before = transport_pass.balance

#         update_pass = await self.transport_repository.debit_balance(
#             user_id = user_id,
#             amount = amount
#         )

#         transaction = Transaction(
#             user_id = user_id,
#             type = TransactionType.USE,
#             amount = amount,
#             balance_before = balance_before,
#             balance_after = update_pass.balance
#         )
#         await self.transaction_repository.create(transaction)

#         return update_pass.balance