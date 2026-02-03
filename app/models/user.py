from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

class User(BaseModel):
    id: ObjectId = Field(default_factory = ObjectId, alias = "_id")
    email: EmailStr
    password: str

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
