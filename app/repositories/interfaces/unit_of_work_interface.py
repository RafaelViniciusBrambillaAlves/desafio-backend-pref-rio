from abc import ABC, abstractmethod
from app.repositories.interfaces.user_repository_interface import IUserRepository


class IUnitOfWork(ABC):

    users: IUserRepository

    @abstractmethod
    async def __aenter__(self):
        pass 

    @abstractmethod    
    async def __aexit__(self, exc_type, exc, tb):
        pass 
    
    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
    

