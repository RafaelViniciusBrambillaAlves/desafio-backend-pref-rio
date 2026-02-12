from abc import ABC, abstractmethod
from app.models.user import User 

class IUserRepository(ABC):

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> User | None:
        pass

    @abstractmethod
    async def delete_by_id(self, id: str) -> User | None:
        pass