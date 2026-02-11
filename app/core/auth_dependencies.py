from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.core.jwt import JWTService
from app.core.exceptions import AppException
from fastapi.security import HTTPAuthorizationCredentials
from app.core.security_scheme import bearer_schemas
from jose import JWTError
from app.models.user import User
from app.services.user_service import UserService
from app.dependencies.user_dependencies import get_user_service

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_schemas),
        auth_services: UserService = Depends(get_user_service)
) -> User:
    
    token = credentials.credentials

    try: 
        payload = JWTService.decode_token(token)
    except JWTError:
        raise AppException(
            error = "INVALID_TOKEN",
            message = "Invalid or maloformed acces token",
            status_code = status.HTTP_401_UNAUTHORIZED
        )


    if payload.get("type") != "access":
        raise AppException(
            error = "INVALID_TOKEN_TYPE",
            message = "Access token required.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )

    user = await auth_services.get_user(payload.get("sub"))

    if not user:
        raise AppException(
            error = "USER_NOT_FOUND",
            message = "User not found.",
            status_code = status.HTTP_401_UNAUTHORIZED
        )

    return user
