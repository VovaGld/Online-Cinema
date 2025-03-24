from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, HttpUrl
from starlette.datastructures import URLPath


class OrderCreateResponseSchema(BaseModel):
    order_id: int
    total_price: Decimal
    status: str
    payment_url: str
    cancel_url: Optional[HttpUrl] = None
    message: Optional[str] = None


class OrderListSchema(BaseModel):
    orders: list[OrderCreateResponseSchema]
