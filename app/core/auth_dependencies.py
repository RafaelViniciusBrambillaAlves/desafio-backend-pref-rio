from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.core.jwt import JWTService
from app.core.exceptions import AppException
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = JWTService.decode_token(token)

    if payload.get("type") != "access":
        raise AppException(
            error="INVALID_TOKEN_TYPE",
            message="Access token required.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    user = await UserRepository.get_by_id(payload.get("sub"))

    if not user:
        raise AppException(
            error="USER_NOT_FOUND",
            message="User not found.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return user
