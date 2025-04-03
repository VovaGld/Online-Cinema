from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import GenreModel
from schemas.movie import BaseCreateSchema


class GenreRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, genre: BaseCreateSchema):
        db_genre = GenreModel(name=genre.name)
        self.db.add(db_genre)
        await self.db.commit()
        await self.db.refresh(db_genre)
        return db_genre

    async def get(self, genre_id: int):
        result = await self.db.execute(
            select(GenreModel).where(GenreModel.id == genre_id)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(GenreModel))
        return result.scalars().all()

    async def delete(self, genre_id: int):
        genre = self.get(genre_id)
        if genre:
            await self.db.delete(genre)
            await self.db.commit()
        return genre
