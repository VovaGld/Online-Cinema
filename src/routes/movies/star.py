from fastapi import APIRouter, Depends, HTTPException

from dependencies.movies import get_star_service
from schemas.movie import BaseCreateSchema, BaseResponseSchema
from services.movie_service.star import StarService

router = APIRouter()


@router.post("/", response_model=BaseResponseSchema)
async def create_star(
    star: BaseCreateSchema, star_service: StarService = Depends(get_star_service)
):
    if await star_service.is_admin():
        return await star_service.create_star(star)
    raise HTTPException(status_code=403, detail="You haven't appropriate permission")


@router.get("/{star_id}", response_model=BaseResponseSchema)
async def read_star(
    star_id: int, star_service: StarService = Depends(get_star_service)
):
    db_star = await star_service.get_star(star_id)
    if db_star is None:
        raise HTTPException(status_code=404, detail="star not found")
    return db_star


@router.get("/", response_model=list[BaseResponseSchema])
async def read_stars(star_service: StarService = Depends(get_star_service)):
    return await star_service.get_all_stars()


@router.delete("/{star_id}", response_model=BaseResponseSchema)
async def delete_star(
    star_id: int, star_service: StarService = Depends(get_star_service)
):
    db_star = await star_service.delete_star(star_id)
    if not await star_service.is_admin():
        raise HTTPException(
            status_code=403, detail="You haven't appropriate permission"
        )
    if db_star is None:
        raise HTTPException(status_code=404, detail="star not found")
    return db_star
