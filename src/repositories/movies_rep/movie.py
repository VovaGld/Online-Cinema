from tkinter.tix import Select

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MovieModel, GenreModel, StarModel, DirectorModel, CertificationModel
from schemas.movie import MovieCreateSchema


class MovieRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, movie: MovieCreateSchema):
        genres = [GenreModel(name=genre.name) for genre in movie.genres]
        stars = [StarModel(name=star.name) for star in movie.stars]
        directors = [DirectorModel(name=director.name) for director in movie.directors]
        certification = CertificationModel(name=movie.certification.name)

        db_movie = MovieModel(
            name=movie.name,
            year=movie.year,
            time=movie.time,
            imdb=movie.imdb,
            votes=movie.votes,
            meta_score=movie.meta_score,
            gross=movie.gross,
            description=movie.description,
            price=movie.price,
            genres=genres,
            stars=stars,
            directors=directors,
            certification=certification
        )
        self.db.add(db_movie)
        await self.db.commit()
        await self.db.refresh(db_movie)
        return db_movie

    async def get(self, movie_id: int):
        result = await self.db.execute(select(MovieModel).where(MovieModel.id == movie_id))
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(select(MovieModel))
        return result.scalars().all

    def delete(self, product_id: int):
        product = self.get(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
        return product
