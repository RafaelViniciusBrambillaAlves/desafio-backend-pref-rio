from pydantic import BaseModel
from bson import ObjectId
from app.domain.transaction_type import TransactionType
from datetime import datetime

class TransactionResponse(BaseModel):
    id: str 
    type: TransactionType
    amount: float
    balance_before: float
    balance_after: float
    created_at: datetime 