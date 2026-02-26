from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_serializer
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        populate_by_name = True
    )

    id: Optional[ObjectId] = Field(default=None, alias="_id")
    email: EmailStr
    password: Optional[str] = None
    provider: str = "local"

