from fastapi import FastAPI
from app.api.routes import users

app = FastAPI(
    title="Backend API",
    version="1.0.0"
)

app.include_router(users.router)