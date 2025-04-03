from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import UserPurchasedMoviesModel
from database.models import (
    DirectorModel,
    GenreModel,
    MovieModel,
    StarModel,
)
from schemas.movie import MovieCreateSchema


class MovieRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, movie: MovieCreateSchema):
        genres = await self.db.execute(
            select(GenreModel).where(GenreModel.id.in_(movie.genres))
        )
        stars = await self.db.execute(
            select(StarModel).where(StarModel.id.in_(movie.stars))
        )
        directors = await self.db.execute(
            select(DirectorModel).where(DirectorModel.id.in_(movie.directors))
        )

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
            genres=list(genres.scalars()),
            stars=list(stars.scalars()),
            directors=list(directors.scalars()),
            certification_id=movie.certification_id,
        )
        self.db.add(db_movie)
        await self.db.commit()
        await self.db.refresh(
            db_movie, ["genres", "stars", "directors", "certification", "comments"]
        )
        return db_movie

    async def get(self, movie_id: int):
        result = await self.db.execute(
            select(MovieModel)
            .options(
                joinedload(MovieModel.genres),
                joinedload(MovieModel.stars),
                joinedload(MovieModel.directors),
                joinedload(MovieModel.comments),
                joinedload(MovieModel.certification),
            )
            .where(MovieModel.id == movie_id)
        )
        return result.scalars().first()

    async def get_movies_with_params(
        self,
        page: int = 1,
        page_size: int = 10,
        name: str = None,
        year: int = None,
        rating: float = None,
        sort_by: str = None,
    ):
        query = select(MovieModel).options(
            joinedload(MovieModel.genres),
            joinedload(MovieModel.stars),
            joinedload(MovieModel.directors),
            joinedload(MovieModel.comments),
            joinedload(MovieModel.certification),
        )

        if name:
            query = query.filter(MovieModel.name.ilike(f"%{name}%"))
        if year:
            query = query.filter(MovieModel.year == year)
        if rating:
            query = query.filter(MovieModel.imdb >= rating)

        if sort_by:
            if sort_by == "price":
                query = query.order_by(MovieModel.price)
            elif sort_by == "release_year":
                query = query.order_by(MovieModel.year)
            elif sort_by == "popularity":
                query = query.order_by(MovieModel.votes.desc())

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await self.db.execute(query)
        movies = result.unique().scalars().all()

        total_query = await self.db.execute(
            select(func.count()).select_from(MovieModel)
        )
        total = total_query.scalar()

        return movies, total

    async def delete(self, movie_id: int):
        movie = self.get(movie_id)
        if movie:
            await self.db.delete(movie)
            await self.db.commit()
        return movie

    async def increment_likes(self, movie_id: int):
        await self.db.execute(
            update(MovieModel)
            .where(MovieModel.id == movie_id)
            .values(likes=MovieModel.likes + 1)
        )
        await self.db.commit()

    async def increment_dislikes(self, movie_id: int):
        await self.db.execute(
            update(MovieModel)
            .where(MovieModel.id == movie_id)
            .values(dislikes=MovieModel.dislikes + 1)
        )
        await self.db.commit()

    async def rate_movie(self, movie_id: int, user_rating: float):
        movie = await self.db.get(MovieModel, movie_id)
        if movie is None:
            raise ValueError("Movie not found")

        if not (1 <= user_rating <= 10):
            raise ValueError("Rating must be between 1 and 10")

        if movie.rate == 0:
            movie.rate = user_rating
        else:
            current_rating = movie.rate
            rate_count = movie.rate_count if movie.rate_count else 1
            new_average = round(
                ((current_rating * rate_count) + user_rating) / (rate_count + 1), 2
            )
            movie.rate = new_average
            movie.rate_count = rate_count + 1

        await self.db.commit()

    async def movie_exists_in_purchases(self, movie_id: int) -> bool:
        query = select(UserPurchasedMoviesModel).where(
            UserPurchasedMoviesModel.c.movie_id == movie_id
        )
        result = await self.db.execute(query)
        return True if result.scalar() else False
