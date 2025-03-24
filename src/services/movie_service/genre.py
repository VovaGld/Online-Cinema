from sqlalchemy.ext.asyncio import AsyncSession

from repositories.movies_rep.genre import GenreRepository
from schemas.movie import BaseCreateSchema


class GenreService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = GenreRepository(db)

    def create_genre(self, genre: BaseCreateSchema):
        return self.repository.create(genre)

    def get_genre(self, genre_id: int):
        return self.repository.get(genre_id)

    def get_all_genres(self):
        return self.repository.get_all()

    def delete_genre(self, genre_id: int):
        return self.repository.delete(genre_id)
