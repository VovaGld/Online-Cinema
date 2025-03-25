from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.movie import BaseResponseSchema, BaseCreateSchema
from services.movie_service.director import DirectorService

router = APIRouter()

@router.post("/", response_model=BaseResponseSchema)
async def create_director(director: BaseCreateSchema, db: AsyncSession = Depends(get_db)):
    service = DirectorService(db)
    return await service.create_director(director)

@router.get("/{director_id}", response_model=BaseResponseSchema)
async def read_director(director_id: int, db: AsyncSession = Depends(get_db)):
    service = DirectorService(db)
    db_director = await service.get_director(director_id)
    if db_director is None:
        raise HTTPException(status_code=404, detail="director not found")
    return db_director

@router.get("/", response_model=list[BaseResponseSchema])
async def read_directors(db: AsyncSession = Depends(get_db)):
    service = DirectorService(db)
    return await service.get_all_directors()

@router.delete("/{director_id}", response_model=BaseResponseSchema)
async def delete_director(director_id: int, db: AsyncSession = Depends(get_db)):
    service = DirectorService(db)
    db_director = await service.delete_director(director_id)
    if db_director is None:
        raise HTTPException(status_code=404, detail="director not found")
    return db_director
