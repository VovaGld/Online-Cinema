from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import StarModel
from schemas.movie import BaseCreateSchema


class StarRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, star: BaseCreateSchema):
        db_star = StarModel(name=star.name)
        self.db.add(db_star)
        await self.db.commit()
        await self.db.refresh(db_star)
        return db_star

    async def get(self, star_id: int):
        result = await self.db.execute(select(StarModel).where(StarModel.id == star_id))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(StarModel))
        return result.scalars().all()

    async def delete(self, star_id: int):
        star = self.get(star_id)
        if star:
            await self.db.delete(star)
            await self.db.commit()
        return star
