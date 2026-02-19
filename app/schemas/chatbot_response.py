from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
from app.domain.chatbot_state import ChatbotState

class ChatbotResponseType(str, Enum):
    INFO = "info"
    QUESTION = "question"
    ACTION = "action"
    ERROR = "error"

class ChatbotResponse(BaseModel):
    intent: str
    type: ChatbotResponseType
    message: str
    next_state: ChatbotState | None = None
    temp_amount: float | None = None
    reset_context: bool = False