from enum import Enum 

class TransactionType(str, Enum):
    RECHARGE = "recharge"
    USE = "use"