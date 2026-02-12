from fastapi import APIRouter, status, Depends, UploadFile, File
from app.schemas.user import UserCreate, UserReponse
from app.services.user_service import UserService 
from app.schemas.response import SucessResponse
from app.core.auth_dependencies import get_current_user
from app.models.user import User
from app.schemas.document import DocumentItem, DocumentListResponse, DocumentUploadResponse
from app.dependencies.user_dependencies import get_user_service
from app.dependencies.database_dependencies import get_database
from app.services.document_services import DocumentService
from app.dependencies.document_dependencies import get_document_service

router = APIRouter(prefix = "/users", tags = ["users"])

@router.post(
    "/",
    status_code = status.HTTP_201_CREATED,
    response_model = SucessResponse[UserReponse]
)
async def create_user(
        user: UserCreate,
        service: UserService = Depends(get_user_service),
        db = Depends(get_database)
):
    created_user  = await service.register(user)

    return SucessResponse(
        message = "User created successfully.",
        data = UserReponse(
            id = str(created_user.id),
            email = created_user.email
        )
    )

@router.get(
    "/{id}",
    status_code = status.HTTP_200_OK,
    response_model = SucessResponse[UserReponse]
)
async def get_user_by_id(
    id: str, 
    service: UserService = Depends(get_user_service),
    _: User = Depends(get_current_user)
):
    user = await service.get_user(id)

    return SucessResponse(
        message = "User found.",
        data = UserReponse(
            id = str(user.id),
            email = user.email
        )
    )

@router.delete(
    "/me",
    status_code = status.HTTP_200_OK,
    response_model = SucessResponse[UserReponse]
)
async def delete_user_by_id(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    deleted_user = await service.delete_user(current_user.id)

    return SucessResponse(
        message = "User deleted successfully",
        data = UserReponse(
            id = str(deleted_user.id),
            email = deleted_user.email
        )
    )
    
@router.post(
    "/me/cnh-photo",
    status_code = status.HTTP_201_CREATED,
    response_model = SucessResponse[DocumentUploadResponse]
)
async def upload_documents(
    file: UploadFile = File(...), 
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service)
):

    path = await document_service.upload(
        user = str(current_user.id),
        file = file
    )

    return SucessResponse(
        message = "Document upload successfuly.",
        data = DocumentUploadResponse(path = path)
    )

@router.get(
    "/me/documents",
    status_code = status.HTTP_200_OK,
    response_model = SucessResponse[DocumentListResponse]
)
async def list_my_documents(
    current_user: User = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service)
):
    documents = await document_service.list_user_documents(
        user_id = str(current_user.id)
    )

    return SucessResponse(
        message = "Documents listed successfully.",
        data = DocumentListResponse(
            documents =[DocumentItem(path = doc) for doc in documents]
        )
    )