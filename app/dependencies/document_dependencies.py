from fastapi import Depends
from app.repositories.document_repository import MinioDocumentStorage
from minio import Minio
from app.core.minio import get_minio_client
from app.application.use_cases.document.upload_document_use_case import UploadDocumentUseCase
from app.application.use_cases.document.list_user_documents_use_case import ListUserDocumentsUseCase
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork
from app.dependencies.database_dependencies import get_unit_of_work

def get_document_storage(
        client: Minio = Depends(get_minio_client)
    ) -> MinioDocumentStorage:

    return MinioDocumentStorage(client)

def get_upload_document_use_case(
        uow: IUnitOfWork = Depends(get_unit_of_work), 
        storage: MinioDocumentStorage = Depends(get_document_storage)
    ) -> UploadDocumentUseCase:

    return UploadDocumentUseCase(uow, storage)

def get_list_user_documents_use_case(
        uow: IUnitOfWork = Depends(get_unit_of_work)
    ) -> ListUserDocumentsUseCase:

    return ListUserDocumentsUseCase(uow)