from pydantic import BaseModel, Field
from bson import ObjectId

class TransportPass(BaseModel):
    id: ObjectId = Field(default_factory = ObjectId, alias = "_id")
    user_id: ObjectId
    balance: float = 0.0

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        

