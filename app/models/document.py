from pydantic import BaseModel, Field, ConfigDict, field_serializer
from bson import ObjectId
from datetime import datetime, UTC

class Document(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    id: ObjectId | None = Field(default = None, alias = "_id")
    user_id: ObjectId
    object_name: str
    content_type: str
    created_at: datetime = Field(default_factory = lambda: datetime.now(UTC))
