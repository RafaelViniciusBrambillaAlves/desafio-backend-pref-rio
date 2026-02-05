from app.core.minio import get_minio_client
from app.core.config import settings
from fastapi import UploadFile
from minio.error import S3Error

class DocumentRepository:

    @staticmethod
    def ensure_bucket_exists(client):
        try: 
            if not client.bucket_exists(settings.MINIO_BUCKET):
                client.make_bucket(settings.MINIO_BUCKET)
        except S3Error as e:
            raise
        

    @staticmethod
    def insert_image(object_name: str, file: UploadFile) -> str:
        client = get_minio_client()
        DocumentRepository.ensure_bucket_exists(client)

        client.put_object(
            bucket_name = settings.MINIO_BUCKET,
            object_name = object_name,
            data = file.file,
            length = -1,
            part_size = 10 * 1024 * 1024,
            content_type = file.content_type
        )
    
        return object_name