from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, HttpUrl

from schemas.movie import BaseResponseSchema


class OrderSchema(BaseModel):
    datetime: datetime
    movies: list[BaseResponseSchema]
    total_price: Decimal
    status: str
    cancel_url: Optional[HttpUrl] = None


class OrderListSchema(BaseModel):
    orders: list[OrderSchema]
