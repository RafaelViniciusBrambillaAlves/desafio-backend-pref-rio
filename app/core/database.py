from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

class MongoDatabase:

    def __init__(self):
        settings = get_settings()
        self.client = AsyncIOMotorClient(settings.DATABASE_URL)
        self.db = self.client[settings.DB_NAME]
    
    def get_database(self):
        return self.db
    
    async def close(self):
        self.client.close() 