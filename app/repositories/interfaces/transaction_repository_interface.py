from abc import ABC, abstractmethod
from app.models.transaction import Transaction
from bson import ObjectId

class ITransactionRepository(ABC):

    @abstractmethod
    async def create(transaction: Transaction) -> Transaction:
        pass
    
    @abstractmethod
    async def list_by_user(user_id: ObjectId, limit: int = 20):
       pass