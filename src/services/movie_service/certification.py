from sqlalchemy.ext.asyncio import AsyncSession

from repositories.movies_rep.certification import CertificationRepository
from schemas.movie import BaseCreateSchema


class CertificationService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = CertificationRepository(db)

    def create_certification(self, certification: BaseCreateSchema):
        return self.repository.create(certification)

    def get_certification(self, certification_id: int):
        return self.repository.get(certification_id)

    def get_all_certifications(self):
        return self.repository.get_all()

    def delete_certification(self, certification_id: int):
        return self.repository.delete(certification_id)
