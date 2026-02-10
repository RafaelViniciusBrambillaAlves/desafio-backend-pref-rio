from enum import Enum

class ChatbotState(str, Enum):
    IDLE = "idle"
    WAITING_RECHARGE_AMOUNT = "waiting_recharge_amount"
    CONFIRM_RECHARGE = "confirm_recharge"