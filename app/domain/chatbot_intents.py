from enum import Enum

class ChatbotIntent(str, Enum):
    GREETING = "greeting"
    CHECK_BALANCE = "check_balance"
    RECHARGE = "recharge"
    UNKNOWN = "unknown"