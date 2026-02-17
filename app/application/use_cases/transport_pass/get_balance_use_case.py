from bson import ObjectId
from app.repositories.interfaces.transportpass_pass_repository_interface import ITransportPassRepository

class GetBalanceUseCase:

    def __init__(self, repository: ITransportPassRepository):
        self._repository = repository

    async def execute(self, user_id: ObjectId) -> float:
        transport_pass = await self._repository.get_by_user_id(user_id)

        if not transport_pass:
            transport_pass = await self._repository.create(user_id)

        return transport_pass.balance