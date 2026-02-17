from app.repositories.interfaces.documents_repository_interface import IDocumentRepository

class ListUserDocumentsUseCase:

    def __init__(self, repository: IDocumentRepository):
        self._repository = repository

    async def execute(self, user_id: str):
        prefix = f"documents/{user_id}/"
        return await self._repository.list_by_prefix(prefix)