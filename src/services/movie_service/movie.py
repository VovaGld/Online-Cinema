from sqlalchemy.ext.asyncio import AsyncSession

from repositories.movies_rep.movie import MovieRepository
from schemas.movie import MovieCreateSchema


class MovieService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = MovieRepository(db)

    def create_movie(self, movie: MovieCreateSchema):
        return self.repository.create(movie)

    def get_movie(self, movie_id: int):
        return self.repository.get(movie_id)

    def get_all_movies(self):
        return self.repository.get_all()

    def delete_movie(self, movie_id: int):
        return self.repository.delete(movie_id)
