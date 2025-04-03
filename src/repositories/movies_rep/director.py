from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import DirectorModel
from schemas.movie import BaseCreateSchema


class DirectorRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, director: BaseCreateSchema):
        db_director = DirectorModel(name=director.name)
        self.db.add(db_director)
        await self.db.commit()
        await self.db.refresh(db_director)
        return db_director

    async def get(self, director_id: int):
        result = await self.db.execute(
            select(DirectorModel).where(DirectorModel.id == director_id)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(DirectorModel))
        return result.scalars().all()

    async def delete(self, director_id: int):
        director = self.get(director_id)
        if director:
            await self.db.delete(director)
            await self.db.commit()
        return director
