from app.models.transaction import Transaction
from bson import ObjectId
from app.repositories.interfaces.transaction_repository_interface import ITransactionRepository
from typing import List
from app.repositories.base_repository import BaseMongoRepository

class TransactionRepository(BaseMongoRepository, ITransactionRepository):

    def __init__(self, database):
        super().__init__(database)

    async def create(self, transaction: Transaction) -> Transaction:
        result = await self._db.transactions.insert_one(
            transaction.model_dump(
                by_alias = True,
                exclude_none = True
            ),
            session = self._session
        )
        transaction.id = result.inserted_id
        return transaction
    
 
    async def list_by_user(self, user_id: ObjectId, limit: int = 20) -> List[Transaction]:
        cursor = (
            self._db.transactions
            .find({"user_id": user_id}, session = self._session)
            .sort("created_at", -1)
            .limit(limit)
        )

        return [Transaction(**doc) async for doc in cursor]