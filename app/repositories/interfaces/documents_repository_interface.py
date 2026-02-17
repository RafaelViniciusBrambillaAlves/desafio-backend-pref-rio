from abc import ABC, abstractmethod
from fastapi import UploadFile

class IDocumentRepository(ABC):

    @abstractmethod
    async def upload(self, object_name: str, file: UploadFile) -> str:
        pass

    @abstractmethod
    async def list_by_prefix(self, prefix: str) -> list[str]:
        pass