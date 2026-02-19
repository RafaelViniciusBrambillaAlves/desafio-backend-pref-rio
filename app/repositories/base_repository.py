from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.client_session import ClientSession
from typing import Optional

class BaseMongoRepository:

    def __init__(self, database: AsyncIOMotorDatabase):
        self._db = database
        self._session: Optional[ClientSession] = None

    def with_session(self, session: ClientSession):
        self._session = session
        return self