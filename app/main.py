from fastapi import FastAPI
from app.api.routes import users, auth, teste, transport_pass, chatbot, transactions
from app.core.database import MongoDatabase
from contextlib import asynccontextmanager

mongo = MongoDatabase()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = mongo.get_database()
    yield
    await mongo.close()

app = FastAPI(
    title="Backend API",
    version="1.0.0",
    swagger_ui_init_oauth = {},
    lifespan = lifespan

)

app.include_router(users.router)
app.include_router(auth.router)
# app.include_router(teste.router)
app.include_router(transport_pass.router)
app.include_router(chatbot.router)
app.include_router(transactions.router)