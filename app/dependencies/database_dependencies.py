from fastapi import Request
from app.repositories.unit_of_work.mongo_unit_of_work import MongoUnitOfWork

def get_unit_of_work(request: Request):
    database = request.app.state.db
    return MongoUnitOfWork(database)