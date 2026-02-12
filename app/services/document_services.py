import uuid
from fastapi import UploadFile, status
from app.core.exceptions import AppException
from minio.error import S3Error
from app.repositories.interfaces.documents_repository_interface import IDocumentRepository
from app.models.user import User

class DocumentService:

    ALLOWED_TYPES = {
        "image/bmp", 
        "image/png", 
        "image/jpeg"
    }

    def __init__(self, repository: IDocumentRepository):
        self.repository = repository


    async def upload(self, user_id: int, file: UploadFile) -> str:

        if file.content_type not in self.ALLOWED_TYPES:
            raise AppException(
                error = "INVALID_IMAGE_FORMAT",
                message = "Only BMP, PNG and JPEG are allowed.",
                status_code = status.HTTP_406_NOT_ACCEPTABLE
            )
        
        object_name = f"documents/{user_id}/{uuid.uuid4()}-{file.filename}"

        try:
            return self.repository.insert_image(object_name, file)
        except S3Error as e:
            raise AppException(
                error = "MINIO_UPLOAD_ERROR",
                message = "Error uploading CNH photo",
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
    

    async def list_user_documents(self, user_id: str) -> list[str]:
        try:
            return self.repository.list_by_user(user_id)
        except S3Error:
            raise AppException(
                error = "MINIO_LIST_ERROR",
                message = "Error listing documents.",
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from e
        