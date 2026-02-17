from fastapi import Depends
from app.repositories.document_repository import DocumentRepository
from app.repositories.interfaces.documents_repository_interface import IDocumentRepository
from minio import Minio
from app.core.minio import get_minio_client
from app.application.use_cases.document.upload_document_use_case import UploadDocumentUseCase
from app.application.use_cases.document.list_user_documents_use_case import ListUserDocumentsUseCase

def get_document_repository(client: Minio = Depends(get_minio_client)) -> IDocumentRepository:
    return DocumentRepository(client)

def get_upload_document_use_case(repository: IDocumentRepository = Depends(get_document_repository)) -> UploadDocumentUseCase:
    return UploadDocumentUseCase(repository)

def get_list_user_documents_use_case(repository: IDocumentRepository = Depends(get_document_repository)) -> ListUserDocumentsUseCase:
    return ListUserDocumentsUseCase(repository)