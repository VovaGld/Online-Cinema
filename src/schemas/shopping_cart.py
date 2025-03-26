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


class CartItemResponseSchema(BaseModel):
    message: str


class CartDetailSchema(BaseModel):
    id: int
    user_id: int
    create_order_url: Optional[str] = None
    clear_cart_url: Optional[str] = None
    items: List[CartItemDetailSchema]
