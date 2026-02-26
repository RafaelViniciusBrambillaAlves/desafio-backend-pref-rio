from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic import field_serializer, ConfigDict
from typing import Optional

# class TransportPass(BaseModel):
#     id: ObjectId = Field(default_factory = ObjectId, alias = "_id")
#     user_id: ObjectId
#     balance: float = 0.0

#     class Config:
#         arbitrary_types_allowed = True
#         populate_by_name = True
        

class TransportPass(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    id: Optional[ObjectId] = Field(default = None, alias = "_id")
    user_id: ObjectId
    balance: float = 0.0