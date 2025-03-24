from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.movie import MovieCreateSchema, MovieSchema
from services.movie_service.movie import MovieService

router = APIRouter()

@router.post("/", response_model=MovieSchema)
async def create_movie(movie: MovieCreateSchema, db: AsyncSession = Depends(get_db)):
    service = MovieService(db)
    return await service.create_movie(movie)

@router.get("/{movie_id}", response_model=MovieSchema)
async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    service = MovieService(db)
    db_movie = await service.get_movie(movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="movie not found")
    return db_movie

@router.get("/", response_model=list[MovieSchema])
async def read_movies(db: AsyncSession = Depends(get_db)):
    service = MovieService(db)
    return await service.get_all_movies()

@router.delete("/{movie_id}", response_model=MovieSchema)
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    service = MovieService(db)
    db_movie = await service.delete_movie(movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="movie not found")
    return db_movie
