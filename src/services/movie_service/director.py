from sqlalchemy.ext.asyncio import AsyncSession

from repositories.movies_rep.director import DirectorRepository
from schemas.movie import BaseCreateSchema


class DirectorService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = DirectorRepository(db)

    def create_director(self, director: BaseCreateSchema):
        return self.repository.create(director)

    def get_director(self, director_id: int):
        return self.repository.get(director_id)

    def get_all_directors(self):
        return self.repository.get_all()

    def delete_director(self, director_id: int):
        return self.repository.delete(director_id)
