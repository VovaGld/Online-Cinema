from sqlalchemy.ext.asyncio import AsyncSession

from repositories.movies_rep.star import StarRepository
from schemas.movie import BaseCreateSchema


class StarService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = StarRepository(db)

    def create_star(self, star: BaseCreateSchema):
        return self.repository.create(star)

    def get_star(self, star_id: int):
        return self.repository.get(star_id)

    def get_all_stars(self):
        return self.repository.get_all()

    def delete_star(self, star_id: int):
        return self.repository.delete(star_id)
