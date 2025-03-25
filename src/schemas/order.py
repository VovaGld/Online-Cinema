from decimal import Decimal
from typing import Optional

from datetime import datetime

from pydantic import BaseModel, HttpUrl

from schemas.movie import BaseResponseSchema

class OrderSchema(BaseModel):
    datetime: datetime
    movies: list[BaseResponseSchema]
    total_price: Decimal
    status: str
    payment_url: Optional[HttpUrl] = None
    cancel_url: Optional[HttpUrl] = None


class OrderListSchema(BaseModel):
    orders: list[OrderSchema]
