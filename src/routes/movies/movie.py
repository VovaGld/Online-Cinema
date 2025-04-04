from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies.movies import get_movie_service, get_comment_service
from schemas.movie import (
    MovieSchema,
    MovieCreateSchema,
    PaginatedMoviesResponse,
    CommentCreateSchema,
    CommentResponseSchema,
)
from services.movie_service.comment import CommentService

from services.movie_service.movie import MovieService

router = APIRouter()


@router.post("/", response_model=MovieSchema)
async def create_movie(
    movie: MovieCreateSchema, movie_service: MovieService = Depends(get_movie_service)
):
    if await movie_service.is_admin():
        return await movie_service.create_movie(movie)
    raise HTTPException(status_code=403, detail="You haven't appropriate permission")


@router.get("/{movie_id}", response_model=MovieSchema)
async def read_movie(
    movie_id: int, movie_service: MovieService = Depends(get_movie_service)
):
    db_movie = await movie_service.get_movie(movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="movie not found")
    return db_movie


@router.get("/", response_model=PaginatedMoviesResponse)
async def read_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    name: str = Query(None),
    year: int = Query(None),
    rating: float = Query(None),
    sort_by: str = Query(None),
    movie_service: MovieService = Depends(get_movie_service),
):
    paginated_movies = await movie_service.get_movies_with_params(
        page=page,
        page_size=page_size,
    )
    if name or year or rating or sort_by:
        paginated_movies = await movie_service.get_movies_with_params(
            page=page,
            page_size=page_size,
            name=name,
            year=year,
            rating=rating,
            sort_by=sort_by,
        )
    return PaginatedMoviesResponse(**paginated_movies)


@router.delete("/{movie_id}", response_model=MovieSchema)
async def delete_movie(
    movie_id: int, movie_service: MovieService = Depends(get_movie_service)
):
    db_movie = await movie_service.delete_movie(movie_id)
    if not await movie_service.is_admin():
        raise HTTPException(
            status_code=403, detail="You haven't appropriate permission"
        )
    if await movie_service.cant_delete_movie(movie_id):
        raise HTTPException(
            status_code=400,
            detail="Cannot delete movie because it has been purchased by at least one user",
        )
    if db_movie is None:
        raise HTTPException(status_code=404, detail="movie not found")
    return db_movie


@router.post("/movies/{movie_id}/like")
async def like_movie(
    movie_id: int, movie_service: MovieService = Depends(get_movie_service)
):
    await movie_service.like_movie(movie_id)
    return {"message": "Movie liked successfully"}


@router.post("/movies/{movie_id}/dislike")
async def dislike_movie(
    movie_id: int, movie_service: MovieService = Depends(get_movie_service)
):
    await movie_service.dislike_movie(movie_id)
    return {"message": "Movie disliked successfully"}


@router.post("/movies/{movie_id}/rate")
async def rate_movie(
    movie_id: int,
    user_rating: float,
    movie_service: MovieService = Depends(get_movie_service),
):
    if not (1 <= user_rating <= 10):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10")
    await movie_service.rate_movie(movie_id, user_rating)
    return {"message": "Movie rated successfully"}


@router.post("/movies/{movie_id}/leave_comment", response_model=CommentResponseSchema)
async def create_comment(
    comment: CommentCreateSchema,
    movie_id: int,
    comment_service: CommentService = Depends(get_comment_service),
    movie_service: MovieService = Depends(get_movie_service),
):
    new_comment = await comment_service.create_comment(movie_id, comment)

    return new_comment
