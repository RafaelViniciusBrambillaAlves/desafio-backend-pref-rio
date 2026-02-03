from pydantic import BaseModel, EmailStr, Field
from app.schemas.user import UserPublic

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    user: UserPublic 