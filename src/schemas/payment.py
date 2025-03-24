from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from src.database.models.payment import PaymentStatus

class PaymentBase(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    payment_method: str

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = None

class PaymentInDB(PaymentBase):
    id: int
    user_id: int
    status: PaymentStatus
    transaction_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaymentResponse(PaymentInDB):
    pass 