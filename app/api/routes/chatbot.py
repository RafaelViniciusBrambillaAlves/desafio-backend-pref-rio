from fastapi import APIRouter, status, Depends
from app.schemas.response import SucessResponse
from app.schemas.message import MessageRequest
from app.core.auth_dependencies import get_current_user
from app.models.user import User
from app.schemas.chatbot_response import ChatbotResponse
from app.application.use_cases.chatbot.handle_chatbot_message_use_case import HandleChatbotMessageUseCase
from app.dependencies.chatbot_dependencies import get_chatbot_use_case

router = APIRouter(prefix = "/chatbot", tags = ["chatbot"])

@router.post(
    "/message",
    status_code = status.HTTP_200_OK,
    response_model = SucessResponse[ChatbotResponse]
)
async def get_message(
    payload: MessageRequest, 
    current_user: User = Depends(get_current_user),
    use_case: HandleChatbotMessageUseCase = Depends(get_chatbot_use_case)
):
    response = await use_case.execute(payload.message, current_user.id)
    
    return SucessResponse(
        message = "Chatbot response generated successfully",
        data = response
    )

