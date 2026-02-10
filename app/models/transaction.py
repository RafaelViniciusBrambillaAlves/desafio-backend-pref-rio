from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from app.domain.transaction_type import TransactionType

class Transaction(BaseModel):
    id: ObjectId | None = Field(default = None, alias = "_id")
    user_id: ObjectId
    type: TransactionType
    amount: float
    balance_before: float
    balance_after: float
    created_at: datetime = Field(default_factory = datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
