from fastapi import APIRouter, status, Depends, UploadFile, File
from app.schemas.user import UserCreate, UserReponse
from app.schemas.response import SucessResponse
from app.core.auth_dependencies import get_current_user
from app.models.user import User
from app.schemas.document import DocumentItem, DocumentListResponse, DocumentUploadResponse
from app.dependencies.user_dependencies import get_create_user_use_case
from app.application.use_cases.user.create_user_use_case import CreateUserUseCase
from app.dependencies.user_dependencies import get_get_user_use_case
from app.application.use_cases.user.get_user_use_case import GetUserUseCase
from app.dependencies.user_dependencies import get_delete_user_use_case
from app.application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from app.application.use_cases.document.list_user_documents_use_case import ListUserDocumentsUseCase
from app.dependencies.document_dependencies import get_list_user_documents_use_case
from app.application.use_cases.document.upload_document_use_case import UploadDocumentUseCase
from app.dependencies.document_dependencies import get_upload_document_use_case


router = APIRouter(prefix = "/users", tags = ["users"])

@router.post(
    "/",
    status_code = status.HTTP_201_CREATED,
    response_model = SucessResponse[UserReponse]
)
async def create_user(
        user: UserCreate,
        use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    created_user  = await use_case.execute(user)

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
    use_case: GetUserUseCase = Depends(get_get_user_use_case),
    _: User = Depends(get_current_user)
):
    user = await use_case.execute(id)

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
    use_case: DeleteUserUseCase = Depends(get_delete_user_use_case)
):
    deleted_user = await use_case.execute(current_user.id)

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
    use_case: UploadDocumentUseCase = Depends(get_upload_document_use_case)
    
):

    path = await use_case.execute(
        user_id = str(current_user.id),
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
    use_case: ListUserDocumentsUseCase = Depends(get_list_user_documents_use_case)
):
    documents = await use_case.execute(
        user_id = str(current_user.id)
    )

    return SucessResponse(
        message = "Documents listed successfully.",
        data = DocumentListResponse(
            documents =[DocumentItem(path = doc) for doc in documents]
        )
    )