from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from schemas.order import OrderCreateResponseSchema


class BaseResponseSchema(BaseModel):
    id: int
    name: str


class BaseCreateSchema(BaseModel):
    name: str


class CommentResponseSchema(BaseModel):
    id: int
    author: str
    text: str


class CommentCreateSchema(BaseModel):
    text: str


class MovieSchema(BaseResponseSchema):
    uuid: UUID
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float] = None
    gross: Optional[float] = None
    description: str
    price: Decimal
    genres: list[BaseResponseSchema]
    stars: list[BaseResponseSchema]
    directors: list[BaseResponseSchema]
    certification: BaseResponseSchema
    likes: Optional[int] = None
    dislikes: Optional[int] = None
    rate: Optional[int] = None
    comments: Optional[list[CommentResponseSchema]] = None


class MovieCreateSchema(BaseCreateSchema):
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float] = None
    gross: Optional[float] = None
    description: str
    price: Decimal
    genres: list[BaseCreateSchema]
    stars: list[BaseCreateSchema]
    directors: list[BaseCreateSchema]
    certification: BaseCreateSchema
