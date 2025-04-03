from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import CertificationModel
from schemas.movie import BaseCreateSchema


class CertificationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, certification: BaseCreateSchema):
        db_certification = CertificationModel(name=certification.name)
        self.db.add(db_certification)
        await self.db.commit()
        await self.db.refresh(db_certification)
        return db_certification

    async def get(self, certification_id: int):
        result = await self.db.execute(
            select(CertificationModel).where(CertificationModel.id == certification_id)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(CertificationModel))
        return result.scalars().all()

    async def delete(self, certification_id: int):
        certification = self.get(certification_id)
        if certification:
            await self.db.delete(certification)
            await self.db.commit()
        return certification
