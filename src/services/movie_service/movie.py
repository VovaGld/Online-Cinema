from sqlalchemy.ext.asyncio import AsyncSession

from database import UserGroupEnum
from repositories.accounts_rep import UserRepository
from repositories.movies_rep.movie import MovieRepository
from schemas.movie import (
    CommentCreateSchema,
    CommentResponseSchema,
    MovieCreateSchema,
    MovieSchema,
)


class MovieService:
    def __init__(
        self, movie_rep: MovieRepository, user_rep: UserRepository, db: AsyncSession
    ) -> None:
        self.movie_rep = movie_rep
        self.user_rep = user_rep
        self.db = db

    async def create_movie(self, movie: MovieCreateSchema):
        return await self.movie_rep.create(movie)

    async def get_movie(self, movie_id: int):
        return await self.movie_rep.get(movie_id)

    async def get_movies_with_params(
        self, page: int = 1, page_size: int = 10, **kwargs
    ):
        movies, total_items = await self.movie_rep.get_movies_with_params(
            page=page, page_size=page_size, **kwargs
        )
        total_pages = (total_items + page_size - 1) // page_size

        return {
            "movies": [MovieSchema.model_validate(movie) for movie in movies],
            "prev_page": (
                f"/api/movies/?page={page - 1}&per_page={page_size}"
                if page > 1
                else None
            ),
            "next_page": (
                f"/api/movies/?page={page + 1}&per_page={page_size}"
                if page < total_pages
                else None
            ),
            "total_pages": total_pages,
            "total_items": total_items,
        }

    async def delete_movie(self, movie_id: int):
        return await self.movie_rep.delete(movie_id)

    async def like_movie(self, movie_id: int):
        await self.movie_rep.increment_likes(movie_id)

    async def dislike_movie(self, movie_id: int):
        await self.movie_rep.increment_dislikes(movie_id)

    async def rate_movie(self, movie_id: int, user_rating: float):
        await self.movie_rep.rate_movie(movie_id, user_rating)

    async def is_admin(self):
        user = await self.user_rep.get_user_from_token()
        return user.has_group(UserGroupEnum.ADMIN)

    async def create_comment(self, movie_id: int, comment: CommentCreateSchema):
        user = await self.user_rep.get_user_from_token()
        db_comment = CommentModel(user_id=user.id, movie_id=movie_id, text=comment.text)
        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)
        return CommentResponseSchema(
            id=db_comment.id, user_id=user.id, text=db_comment.text
        )

    async def cant_delete_movie(self, movie_id: int) -> bool:
        return await self.movie_rep.movie_exists_in_purchases(movie_id)
