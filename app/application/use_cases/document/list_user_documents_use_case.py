from app.repositories.interfaces.documents_repository_interface import IDocumentRepository
from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork
from bson import ObjectId

class ListUserDocumentsUseCase:

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def execute(self, user_id: ObjectId):
        
        async with self._uow:
            documents = await self._uow.documents.list_by_user(user_id)

        return documents