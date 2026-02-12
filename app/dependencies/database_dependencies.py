from fastapi import Request
from app.core.database import MongoDatabase

def get_database(request: Request):
    return request.app.state.db