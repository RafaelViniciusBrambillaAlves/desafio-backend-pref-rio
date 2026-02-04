from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    id: ObjectId = Field(default_factory = ObjectId, alias = "_id")
    email: EmailStr
    password: Optional[str] = None
    provider: str = "local"

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
