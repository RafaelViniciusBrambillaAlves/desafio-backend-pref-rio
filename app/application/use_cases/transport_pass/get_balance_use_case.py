from bson import ObjectId
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork

class GetBalanceUseCase:

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def execute(self, user_id: ObjectId) -> float:
        async with self._uow:
            transport_pass = await self._uow.transport_passes.get_by_user_id(user_id)

            if not transport_pass:
                transport_pass = await self._uow.transport_passes.create(user_id)

        return transport_pass.balance