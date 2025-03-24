from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.movie import BaseResponseSchema, BaseCreateSchema
from services.movie_service.star import StarService

router = APIRouter()

@router.post("/", response_model=BaseResponseSchema)
async def create_star(star: BaseCreateSchema, db: AsyncSession = Depends(get_db)):
    service = StarService(db)
    return await service.create_star(star)

@router.get("/{star_id}", response_model=BaseResponseSchema)
async def read_star(star_id: int, db: AsyncSession = Depends(get_db)):
    service = StarService(db)
    db_star = await service.get_star(star_id)
    if db_star is None:
        raise HTTPException(status_code=404, detail="star not found")
    return db_star

@router.get("/", response_model=list[BaseResponseSchema])
async def read_stars(db: AsyncSession = Depends(get_db)):
    service = StarService(db)
    return await service.get_all_stars()

@router.delete("/{star_id}", response_model=BaseResponseSchema)
async def delete_star(star_id: int, db: AsyncSession = Depends(get_db)):
    service = StarService(db)
    db_star = await service.delete_star(star_id)
    if db_star is None:
        raise HTTPException(status_code=404, detail="star not found")
    return db_star
