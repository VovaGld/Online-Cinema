from fastapi import APIRouter, Depends, HTTPException

from dependencies.movies import get_certification_service
from schemas.movie import BaseCreateSchema, BaseResponseSchema
from services.movie_service.certification import CertificationService

router = APIRouter()


@router.post("/", response_model=BaseResponseSchema)
async def create_certification(
    certification: BaseCreateSchema,
    certification_service: CertificationService = Depends(get_certification_service),
):
    if await certification_service.is_admin():
        return await certification_service.create_certification(certification)
    raise HTTPException(status_code=403, detail="You haven't appropriate permission")


@router.get("/{certification_id}", response_model=BaseResponseSchema)
async def read_certification(
    certification_id: int,
    certification_service: CertificationService = Depends(get_certification_service),
):
    db_certification = await certification_service.get_certification(certification_id)
    if db_certification is None:
        raise HTTPException(status_code=404, detail="certification not found")
    return db_certification


@router.get("/", response_model=list[BaseResponseSchema])
async def read_certifications(
    certification_service: CertificationService = Depends(get_certification_service),
):
    return await certification_service.get_all_certifications()


@router.delete("/{certification_id}", response_model=BaseResponseSchema)
async def delete_certification(
    certification_id: int,
    certification_service: CertificationService = Depends(get_certification_service),
):
    db_certification = await certification_service.delete_certification(
        certification_id
    )
    if not await certification_service.is_admin():
        raise HTTPException(
            status_code=403, detail="You haven't appropriate permission"
        )
    if db_certification is None:
        raise HTTPException(status_code=404, detail="certification not found")
    return db_certification
