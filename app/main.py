from fastapi import FastAPI
from app.api.routes import users, auth, teste, transport_pass, chatbot

app = FastAPI(
    title="Backend API",
    version="1.0.0",
    swagger_ui_init_oauth = {}

)

app.include_router(users.router)
app.include_router(auth.router)
# app.include_router(teste.router)
app.include_router(transport_pass.router)
app.include_router(chatbot.router)