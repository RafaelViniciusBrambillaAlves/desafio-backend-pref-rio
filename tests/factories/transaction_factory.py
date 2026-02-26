from bson import ObjectId
from datetime import datetime, UTC
from app.models.transaction import Transaction
from app.domain.transaction_type import TransactionType

def transaction_factory(
    *,
    id: str | None = None,
    user_id: ObjectId | None = None,
    type: TransactionType = TransactionType.RECHARGE,
    amount: float = 10,
    balance_before: float = 0,
    balance_after: float = 10,
    created_at: datetime | None = None,
) -> Transaction:
    
    return Transaction(
        id = ObjectId(id) if id else ObjectId(),
        user_id = user_id or ObjectId(),
        type = type,
        amount = amount,
        balance_before = balance_before,
        balance_after = balance_after,
        created_at = created_at or datetime.now(UTC)
    )