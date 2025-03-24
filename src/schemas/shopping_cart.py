from typing import List, Optional

from pydantic import BaseModel


class CartItemCreateSchema(BaseModel):
    movie_id: int


class CartItemDetailSchema(BaseModel):
    id: int
    warning: Optional[str]
    movie_id: int
    title: str
    price: float
    genres: List[str]
    release_year: int


class CartResponseSchema(BaseModel):
    user_id: int
    items: List[CartItemDetailSchema]
