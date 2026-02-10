from app.repositories.transaction_repositoy import TransactionRepository
from bson import ObjectId
from app.schemas.transaction import TransactionResponse

class TransactionService:

    @classmethod
    async def list_transactions(cls, user_id: ObjectId):
        transactions = await TransactionRepository.list_by_user(user_id)

        return [
            TransactionResponse(
                id = str(tx.id),
                type = tx.type,
                amount = tx.amount,
                balance_before = tx.balance_before,
                balance_after = tx.balance_after,
                created_at = tx.created_at
            )
            for tx in transactions
        ]
