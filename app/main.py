from fastapi import FastAPI
from app.api.routes import users, auth, teste

app = FastAPI(
    title="Backend API",
    version="1.0.0",
    swagger_ui_init_oauth = {}

)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(teste.router)