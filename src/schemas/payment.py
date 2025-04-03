from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, HttpUrl


class PaymentSchema(BaseModel):
    datetime: datetime
    amount: Decimal
    status: str
    payment_url: Optional[HttpUrl] = None


class PaymentListSchema(BaseModel):
    payments: list[PaymentSchema]
