from app.repositories.interfaces.documents_repository_interface import IDocumentRepository
from bson import ObjectId
from fastapi import UploadFile, status
from app.core.exceptions import AppException
import uuid
from minio.error import S3Error


class UploadDocumentUseCase:

    ALLOWED_TYPES = {
        "image/bmp",
        "image/png",
        "image/jpeg"
    }

    def __init__(self, repository: IDocumentRepository):
        self._repository = repository

    
    async def execute(self, user_id: ObjectId, file: UploadFile) -> str:

        if file.content_type not in self.ALLOWED_TYPES:
            raise AppException(
                error = "INVALID_IMAGE_FORMAT", 
                message = "Only BMP, PNG and JPEG are allowed.",
                status_code = status.HTTP_406_NOT_ACCEPTABLE
            )
        
        object_name = f"documents/{user_id}/{uuid.uuid4()}"

        return await self._repository.upload(object_name, file)

        