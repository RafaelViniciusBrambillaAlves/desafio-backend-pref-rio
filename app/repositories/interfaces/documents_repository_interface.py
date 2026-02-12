from abc import ABC, abstractmethod
from fastapi import UploadFile

class IDocumentRepository(ABC):

    @abstractmethod
    def ensure_bucket_exists(self, client):
        pass

    @abstractmethod
    def insert_image(self, object_name: str, file: UploadFile) -> str:
        pass

    @abstractmethod
    def list_by_user(self, user_id: str) -> list[str]:
        pass