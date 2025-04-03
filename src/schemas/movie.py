from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class BaseCreateSchema(BaseModel):
    name: str


class CommentResponseSchema(BaseModel):
    id: int
    user_id: int
    text: str

    model_config = {"from_attributes": True}


class CommentCreateSchema(BaseModel):
    text: str


class MovieSchema(BaseModel):
    id: int
    name: str
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
    rate: Optional[float] = None
    rate_count: Optional[int] = None
    comments: Optional[list[CommentResponseSchema]] = None

    model_config = {"from_attributes": True}


class MovieCreateSchema(BaseCreateSchema):
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float] = None
    gross: Optional[float] = None
    description: str
    price: Decimal
    genres: list[int]
    stars: list[int]
    directors: list[int]
    certification_id: int


class PaginatedMoviesResponse(BaseModel):
    movies: list[MovieSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
