from os import getenv
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = getenv("DATABASE_URL")
DB_NAME = getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]