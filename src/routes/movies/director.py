from fastapi import APIRouter, Depends, HTTPException

from dependencies.movies import get_director_service
from schemas.movie import BaseCreateSchema, BaseResponseSchema
from services.movie_service.director import DirectorService

router = APIRouter()


@router.post("/", response_model=BaseResponseSchema)
async def create_director(
    director: BaseCreateSchema,
    director_service: DirectorService = Depends(get_director_service),
):
    if await director_service.is_admin():
        return await director_service.create_director(director)
    raise HTTPException(status_code=403, detail="You haven't appropriate permission")


@router.get("/{director_id}", response_model=BaseResponseSchema)
async def read_director(
    director_id: int, director_service: DirectorService = Depends(get_director_service)
):
    db_director = await director_service.get_director(director_id)
    if db_director is None:
        raise HTTPException(status_code=404, detail="director not found")
    return db_director


@router.get("/", response_model=list[BaseResponseSchema])
async def read_directors(
    director_service: DirectorService = Depends(get_director_service),
):
    return await director_service.get_all_directors()


@router.delete("/{director_id}", response_model=BaseResponseSchema)
async def delete_director(
    director_id: int, director_service: DirectorService = Depends(get_director_service)
):
    db_director = await director_service.delete_director(director_id)
    if not await director_service.is_admin():
        raise HTTPException(
            status_code=403, detail="You haven't appropriate permission"
        )
    if db_director is None:
        raise HTTPException(status_code=404, detail="director not found")
    return db_director
