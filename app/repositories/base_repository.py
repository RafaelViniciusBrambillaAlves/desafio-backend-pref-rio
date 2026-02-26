from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClientSession
from typing import Optional

class BaseMongoRepository:

    def __init__(self, database: AsyncIOMotorDatabase):
        self._db = database
        self._session: Optional[AsyncIOMotorClientSession] = None

    def with_session(self, session: AsyncIOMotorClientSession):
        self._session = session
        return self