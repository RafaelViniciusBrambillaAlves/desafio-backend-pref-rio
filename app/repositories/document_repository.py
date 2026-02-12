from app.core.minio import get_minio_client
from app.core.config import settings
from fastapi import UploadFile
from minio.error import S3Error
from app.repositories.interfaces.documents_repository_interface import IDocumentRepository
from minio import Minio

class DocumentRepository(IDocumentRepository):

    def __init__(self, client: Minio):
        self.client = client

    def ensure_bucket_exists(self) -> None:
         
        if not self.client.bucket_exists(settings.MINIO_BUCKET):
            self.client.make_bucket(settings.MINIO_BUCKET) 

    def insert_image(self, object_name: str, file: UploadFile) -> str:
        try:
            self.ensure_bucket_exists()

            self.client.put_object(
                bucket_name = settings.MINIO_BUCKET,
                object_name = object_name,
                data = file.file,
                length = -1,
                part_size = 10 * 1024 * 1024,
                content_type = file.content_type
            )
    
            return object_name
    
        except S3Error:
            raise

    def list_by_user(self, user_id: str) -> list[str]:
        try:
            prefix = f"documents/{user_id}/"

            objects = self.client.list_objects(
                bucket_name = settings.MINIO_BUCKET,
                prefix = prefix,
                recursive = True
            )
            return [obj.object_name for obj in objects]
        
        except S3Error as e:
            raise

        