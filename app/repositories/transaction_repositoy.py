from app.core.database import db
from app.models.transaction import Transaction
from bson import ObjectId

class TransactionRepository:

    @staticmethod
    async def create(transaction: Transaction) -> Transaction:
        result = await db.transactions.insert_one(
            transaction.model_dump(
                by_alias = True,
                exclude_none = True
            )
        )
        transaction.id = result.inserted_id
        return transaction
    
    @staticmethod
    async def list_by_user(user_id: ObjectId, limit: int = 20):
        cursor = (
            db.transactions
            .find({"user_id": user_id})
            .sort("created_at", -1)
            .limit(limit)
        )

        return [Transaction(**doc) async for doc in cursor]