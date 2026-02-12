from fastapi import Depends
from app.dependencies.database_dependencies import get_database
from app.dependencies.transport_pass_dependecies import get_transport_pass_service
from app.repositories.chatbot_context_repository import ChatbotContextRepository
from app.services.chatbot_service import ChatbotService

def get_chatbot_service(
        db = Depends(get_database),
        transport_service = Depends(get_transport_pass_service)
):
    context_repository = ChatbotContextRepository(db)

    return ChatbotService(
        context_repository = context_repository,
        transport_service = transport_service
    )