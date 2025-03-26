from fastapi import APIRouter, Depends, HTTPException, Query
from dependencies.movies import get_movie_service
from schemas.movie import MovieSchema, MovieCreateSchema, PaginatedMoviesResponse
from services.movie_service.movie import MovieService

router = APIRouter()

@router.post("/", response_model=MovieSchema)
async def create_movie(movie: MovieCreateSchema, movie_service: MovieService = Depends(get_movie_service)):
    if await movie_service.is_admin():
        return await movie_service.create_movie(movie)
    raise HTTPException(status_code=403, detail="You haven't appropriate permission")

@router.get("/{movie_id}", response_model=MovieSchema)
async def read_movie(movie_id: int, movie_service: MovieService = Depends(get_movie_service)):
    db_movie = await movie_service.get_movie(movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="movie not found")
    return db_movie

@router.get("/", response_model=PaginatedMoviesResponse)
async def read_movies(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1),
        movie_service: MovieService = Depends(get_movie_service)
):
    paginated_movies = await movie_service.get_all_movies(page, page_size)
    return PaginatedMoviesResponse(**paginated_movies)

@router.delete("/{movie_id}", response_model=MovieSchema)
async def delete_movie(movie_id: int, movie_service: MovieService = Depends(get_movie_service)):
    db_movie = await movie_service.delete_movie(movie_id)
    if not await movie_service.is_admin():
        raise HTTPException(status_code=403, detail="You haven't appropriate permission")
    if db_movie is None:
        raise HTTPException(status_code=404, detail="movie not found")
    return db_movie
