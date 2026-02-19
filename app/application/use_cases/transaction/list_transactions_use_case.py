from app.repositories.interfaces.transaction_repository_interface import ITransactionRepository
from bson import ObjectId
from app.schemas.transaction import TransactionResponse
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork


class ListTransactionsUseCase:

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def execute(self, user_id: ObjectId):
        
        async with self._uow:

            transactions = await self._uow.transactions.list_by_user(user_id)
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