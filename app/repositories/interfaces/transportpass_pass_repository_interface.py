from abc import ABC, abstractmethod
from bson import ObjectId
from app.models.transport_pass import TransportPass

class ITransportPassRepository(ABC):

    @abstractmethod
    async def get_by_user_id(user_id: ObjectId) -> TransportPass | None:
        pass

    @abstractmethod
    async def create(user_id: ObjectId) -> TransportPass:
        pass

    @abstractmethod
    async def update_balance(user_id: ObjectId, amount: float) -> TransportPass:
        pass

    @abstractmethod
    async def debit_balance(user_id: ObjectId, amount: float) -> TransportPass | None:
        pass