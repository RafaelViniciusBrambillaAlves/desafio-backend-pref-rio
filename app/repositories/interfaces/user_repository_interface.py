from abc import ABC, abstractclassmethod
from app.models.user import User 

class IUserRepository(ABC):

    @abstractclassmethod
    async def create(self, user: User) -> User:
        pass

    @abstractclassmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractclassmethod
    async def get_by_id(self, id: str) -> User | None:
        pass

    @abstractclassmethod
    async def delete_by_id(self, id: str) -> User | None:
        pass