from app.models.transaction import Transaction
from bson import ObjectId
from app.repositories.interfaces.transaction_repository_interface import ITransactionRepository

class TransactionRepository(ITransactionRepository):

    def __init__(self, database):
        self.db = database


    async def create(self, transaction: Transaction) -> Transaction:
        result = await self.db.transactions.insert_one(
            transaction.model_dump(
                by_alias = True,
                exclude_none = True
            )
        )
        transaction.id = result.inserted_id
        return transaction
    
 
    async def list_by_user(self, user_id: ObjectId, limit: int = 20):
        cursor = (
            self.db.transactions
            .find({"user_id": user_id})
            .sort("created_at", -1)
            .limit(limit)
        )

        return [Transaction(**doc) async for doc in cursor]