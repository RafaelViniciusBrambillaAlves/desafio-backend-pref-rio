from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase): 
    password: str

class UserReponse(UserBase):
    id: str

class UserPublic(BaseModel):
    id: str
    email: str
