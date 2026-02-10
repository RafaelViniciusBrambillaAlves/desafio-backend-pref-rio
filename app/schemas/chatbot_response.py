from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class ChatbotResponseType(str, Enum):
    INFO = "info"
    QUESTION = "question"
    ACTION = "action"
    ERROR = "error"

class ChatbotResponse(BaseModel):
    intent: str
    type: ChatbotResponseType
    message: str
    actions: Optional[List[str]] = None