from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime
from app.domain.chatbot_state import ChatbotState

class ChatbotContext(BaseModel):
    user_id: ObjectId
    state: ChatbotState = ChatbotState.IDLE
    temp_amount: Optional[float] = None
    updated_at: datetime = Field(default_factory = datetime.utcnow)

    model_config = {
        "arbitrary_types_allowed": True
    }