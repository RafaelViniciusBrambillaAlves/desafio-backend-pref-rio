from pydantic import BaseModel, Field

class MessageRequest(BaseModel):
    message: str = Field(
        min_length = 1,
        max_length = 100,
        description = "User message sent to chatbot"
    )