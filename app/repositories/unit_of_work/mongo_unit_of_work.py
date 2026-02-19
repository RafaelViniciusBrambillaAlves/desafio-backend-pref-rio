from app.repositories.interfaces.unit_of_work_interface import IUnitOfWork
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.user_repository import MongoUserRepository
from app.repositories.transport_pass_repository import TransportPassRepository
from app.repositories.transaction_repositoy import TransactionRepository
from app.repositories.chatbot_context_repository import ChatbotContextRepository
from app.repositories.document_metadata_repository import DocumentMetadataRepository

class MongoUnitOfWork(IUnitOfWork):

    def __init__(self, database: AsyncIOMotorDatabase):
        self._database = database
        self._session = None

        self.users = MongoUserRepository(database)
        self.transport_passes = TransportPassRepository(database)
        self.transactions = TransactionRepository(database)
        self.chatbot_context = ChatbotContextRepository(database)
        self.documents = DocumentMetadataRepository(database)

    async def __aenter__(self):
        self._session = await self._database.client.start_session()
        self._session.start_transaction()

        self.users.with_session(self._session)
        self.documents.with_session(self._session)
        self.transport_passes.with_session(self._session)
        self.transactions.with_session(self._session)
        self.chatbot_context.with_session(self._session)

        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self._session.end_session()

    async def commit(self):
        await self._session.commit_transaction()

    async def rollback(self):
        await self._session.abort_transaction()


