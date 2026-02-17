from abc import ABC, abstractmethod
from app.models.transaction import Transaction
from bson import ObjectId
from typing import List

class ITransactionRepository(ABC):

    @abstractmethod
    async def create(self, transaction: Transaction) -> Transaction:
        pass
    
    @abstractmethod
    async def list_by_user(self, user_id: ObjectId, limit: int = 20) -> List[Transaction]:
       pass