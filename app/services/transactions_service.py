# from app.repositories.transaction_repositoy import TransactionRepository
# from bson import ObjectId
# from app.schemas.transaction import TransactionResponse
# from app.repositories.interfaces.transaction_repository_interface import ITransactionRepository

# class TransactionService:

#     def __init__(self, repository: ITransactionRepository):
#         self.repository = repository

#     async def list_transactions(self, user_id: ObjectId):
#         transactions = await self.repository.list_by_user(user_id)

#         return [
#             TransactionResponse(
#                 id = str(tx.id),
#                 type = tx.type,
#                 amount = tx.amount,
#                 balance_before = tx.balance_before,
#                 balance_after = tx.balance_after,
#                 created_at = tx.created_at
#             )
#             for tx in transactions
#         ]
