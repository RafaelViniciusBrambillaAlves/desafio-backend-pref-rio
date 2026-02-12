from fastapi import APIRouter, status, Depends
from app.schemas.response import SucessResponse
from app.schemas.message import MessageRequest
from app.services.chatbot_service import ChatbotService
from app.core.auth_dependencies import get_current_user
from app.models.user import User
from app.schemas.chatbot_response import ChatbotResponse
from app.dependencies.chatbot_dependencies import get_chatbot_service

router = APIRouter(prefix = "/chatbot", tags = ["chatbot"])

@router.post(
    "/message",
    status_code = status.HTTP_200_OK,
    response_model = SucessResponse[ChatbotResponse]
)
async def get_message(
    payload: MessageRequest, 
    current_user: User = Depends(get_current_user),
    service: ChatbotService = Depends(get_chatbot_service)
):
    response = await service.handle_message(payload.message, current_user.id)
    
    return SucessResponse(
        message = "Chatbot response generated successfully",
        data = response
    )

