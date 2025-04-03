from fastapi import APIRouter, Depends, HTTPException

from dependencies.movies import get_genre_service
from schemas.movie import BaseCreateSchema, BaseResponseSchema
from services.movie_service.genre import GenreService

router = APIRouter()


@router.post("/", response_model=BaseResponseSchema)
async def create_genre(
    genre: BaseCreateSchema, genre_service: GenreService = Depends(get_genre_service)
):
    if await genre_service.is_admin():
        return await genre_service.create_genre(genre)
    raise HTTPException(status_code=403, detail="You haven't appropriate permission")


@router.get("/{genre_id}", response_model=BaseResponseSchema)
async def read_genre(
    genre_id: int, genre_service: GenreService = Depends(get_genre_service)
):
    db_genre = await genre_service.get_genre(genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="genre not found")
    return db_genre


@router.get("/", response_model=list[BaseResponseSchema])
async def read_genres(genre_service: GenreService = Depends(get_genre_service)):
    return await genre_service.get_all_genres()


@router.delete("/{genre_id}", response_model=BaseResponseSchema)
async def delete_genre(
    genre_id: int, genre_service: GenreService = Depends(get_genre_service)
):
    db_genre = await genre_service.delete_genre(genre_id)
    if not await genre_service.is_admin():
        raise HTTPException(
            status_code=403, detail="You haven't appropriate permission"
        )
    if db_genre is None:
        raise HTTPException(status_code=404, detail="genre not found")
    return db_genre
