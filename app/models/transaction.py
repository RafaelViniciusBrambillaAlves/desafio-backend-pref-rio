from datetime import datetime, UTC
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from bson import ObjectId
from app.domain.transaction_type import TransactionType

class Transaction(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    id: ObjectId | None = Field(default = None, alias = "_id")
    user_id: ObjectId
    type: TransactionType
    amount: float
    balance_before: float
    balance_after: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
