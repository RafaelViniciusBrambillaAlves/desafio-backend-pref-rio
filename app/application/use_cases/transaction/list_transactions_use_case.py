from app.repositories.interfaces.transaction_repository_interface import ITransactionRepository
from bson import ObjectId
from app.schemas.transaction import TransactionResponse


class ListTransactionsUseCase:

    def __init__(self, repository: ITransactionRepository):
        self._repository = repository

    async def execute(self, user_id: ObjectId):

        transactions = await self._repository.list_by_user(user_id)

        return [
            TransactionResponse(
                id = str(tx.id),
                type = tx.type,
                amount = tx.amount,
                balance_before = tx.balance_before,
                balance_after = tx.balance_after,
                created_at = tx.created_at
            )
            for tx in transactions
        ]