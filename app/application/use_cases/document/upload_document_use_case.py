from app.repositories.interfaces.documents_repository_interface import IDocumentRepository
from bson import ObjectId
from fastapi import UploadFile, status
from app.core.exceptions import AppException
import uuid
from minio.error import S3Error
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork
from app.models.document import Document


class UploadDocumentUseCase:

    ALLOWED_TYPES = {
        "image/bmp",
        "image/png",
        "image/jpeg"
    }

    def __init__(self, uow: IUnitOfWork, storage):
        self._uow = uow
        self._storage = storage

    
    async def execute(self, user_id: ObjectId, file: UploadFile) -> str:

        if file.content_type not in self.ALLOWED_TYPES:
            raise AppException(
                error = "INVALID_IMAGE_FORMAT", 
                message = "Only BMP, PNG and JPEG are allowed.",
                status_code = status.HTTP_406_NOT_ACCEPTABLE
            )
        
        object_name = f"documents/{user_id}/{uuid.uuid4()}"

        async with self._uow:

            await self._storage.upload(object_name, file)

            document = Document(
                user_id = user_id, 
                object_name = object_name,
                content_type = file.content_type
            )

            await self._uow.documents.create(document)
        
        return object_name
        