from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.movie import BaseResponseSchema, BaseCreateSchema
from services.movie_service.genre import GenreService

router = APIRouter()

@router.post("/", response_model=BaseResponseSchema)
async def create_genre(genre: BaseCreateSchema, db: AsyncSession = Depends(get_db)):
    service = GenreService(db)
    return await service.create_genre(genre)

@router.get("/{genre_id}", response_model=BaseResponseSchema)
async def read_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    service = GenreService(db)
    db_genre = await service.get_genre(genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="genre not found")
    return db_genre

@router.get("/", response_model=list[BaseResponseSchema])
async def read_genres(db: AsyncSession = Depends(get_db)):
    service = GenreService(db)
    return await service.get_all_genres()

@router.delete("/{genre_id}", response_model=BaseResponseSchema)
async def delete_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    service = GenreService(db)
    db_genre = await service.delete_genre(genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="genre not found")
    return db_genre
