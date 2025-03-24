from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.movie import BaseResponseSchema, BaseCreateSchema
from services.movie_service.certification import CertificationService

router = APIRouter()

@router.post("/", response_model=BaseResponseSchema)
async def create_certification(certification: BaseCreateSchema, db: AsyncSession = Depends(get_db)):
    service = CertificationService(db)
    return await service.create_certification(certification)

@router.get("/{certification_id}", response_model=BaseResponseSchema)
async def read_certification(certification_id: int, db: AsyncSession = Depends(get_db)):
    service = CertificationService(db)
    db_certification = await service.get_certification(certification_id)
    if db_certification is None:
        raise HTTPException(status_code=404, detail="certification not found")
    return db_certification

@router.get("/", response_model=list[BaseResponseSchema])
async def read_certifications(db: AsyncSession = Depends(get_db)):
    service = CertificationService(db)
    return await service.get_all_certifications()

@router.delete("/{certification_id}", response_model=BaseResponseSchema)
async def delete_certification(certification_id: int, db: AsyncSession = Depends(get_db)):
    service = CertificationService(db)
    db_certification = await service.delete_certification(certification_id)
    if db_certification is None:
        raise HTTPException(status_code=404, detail="certification not found")
    return db_certification
