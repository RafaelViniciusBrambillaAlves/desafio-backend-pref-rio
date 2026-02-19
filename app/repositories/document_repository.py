from app.core.minio import get_minio_client
from app.core.config import settings
from fastapi import UploadFile
from minio.error import S3Error
from app.repositories.interfaces.documents_repository_interface import IDocumentRepository
from minio import Minio
from fastapi.concurrency import run_in_threadpool

class MinioDocumentStorage(IDocumentRepository):

    def __init__(self, client: Minio):
        self._client = client
        self._bucket = settings.MINIO_BUCKET

    async def _ensure_bucket_exists(self):
        exists = await run_in_threadpool(
            self._client.bucket_exists,
            self._bucket  
        )

        if not exists:
            await run_in_threadpool(
                self._client.make_bucket,
                self._bucket
            )


    async def upload(self, object_name: str, file: UploadFile) -> str:
        await self._ensure_bucket_exists()

        await run_in_threadpool(
           self._client.put_object,
           self._bucket,
           object_name,
           file.file,
           -1, 
           part_size = 10 * 1024 * 1024,
           content_type = file.content_type
        )
        
        return object_name


    async def list_by_prefix(self, prefix: str) -> list[str]:
        objects = await run_in_threadpool(
            self._client.list_objects,
            self._bucket,
            prefix,
            True
        )

        return [obj.object_name for obj in objects]