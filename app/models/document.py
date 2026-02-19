from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from datetime import datetime

class Document(BaseModel):
    id: ObjectId | None = Field(default = None, alias = "_id")
    user_id: ObjectId
    object_name: str
    content_type: str
    created_at: datetime = Field(default_factory = datetime.utcnow)

    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        json_encoders = {ObjectId: str}
    )