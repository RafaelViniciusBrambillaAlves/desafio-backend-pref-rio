from fastapi import APIRouter, status, Depends
from app.schemas.user import UserCreate, UserReponse
from app.services.user_service import UserService 
from app.schemas.response import SucessResponse

router = APIRouter(prefix = "/users", tags = ["users"])

@router.post(
    "/",
    status_code = status.HTTP_201_CREATED,
    response_model = SucessResponse[UserReponse]
)
async def create_user(user: UserCreate):
    created_user  = await UserService.register(user)

    return SucessResponse(
        message = "User created successfully.",
        data = UserReponse(
            id = str(created_user.id),
            email = created_user.email
        )
    )
