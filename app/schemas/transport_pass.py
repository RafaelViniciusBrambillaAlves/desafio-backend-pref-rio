from pydantic import BaseModel, Field

class BalanceResponse(BaseModel):
    balance: float

class RechargeRequest(BaseModel):
    amount: float

class DebitRequest(BaseModel):
    amount: float = Field(gt = 0, description = "Amount to debit from balance")
