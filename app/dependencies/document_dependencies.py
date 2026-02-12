from fastapi import Depends
from app.repositories.document_repository import DocumentRepository
from app.services.document_services import DocumentService
from app.repositories.interfaces.documents_repository_interface import IDocumentRepository
from minio import Minio
from app.core.minio import get_minio_client

def get_document_repository(client: Minio = Depends(get_minio_client)) -> IDocumentRepository:
    return DocumentRepository(client)

def get_document_service(repository: IDocumentRepository = Depends(get_document_repository)) -> DocumentService:
    return DocumentService(repository)