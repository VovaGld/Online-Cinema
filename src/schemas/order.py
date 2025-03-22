from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class OrderCreateResponseSchema(BaseModel):
    order_id: int
    total_price: Decimal
    status: str
    payment_url: str
    message: Optional[str] = None