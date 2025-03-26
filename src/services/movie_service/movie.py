from database import UserGroupEnum
from repositories.accounts_rep import UserRepository
from repositories.movies_rep.movie import MovieRepository
from schemas.movie import MovieCreateSchema, MovieSchema


class MovieService:
    def __init__(
            self,
            movie_rep: MovieRepository,
            user_rep: UserRepository
    ) -> None:
        self.movie_rep = movie_rep
        self.user_rep = user_rep

    async def create_movie(self, movie: MovieCreateSchema):
        return await self.movie_rep.create(movie)

    async def get_movie(self, movie_id: int):
        return await self.movie_rep.get(movie_id)

    async def get_all_movies(self, page: int = 1, page_size: int = 10):
        movies, total_items = await self.movie_rep.get_all(page, page_size)
        total_pages = (total_items + page_size - 1) // page_size

        return {
            "movies": [MovieSchema.model_validate(movie) for movie in movies],
            "prev_page": f"/api/movies/?page={page - 1}&per_page={page_size}" if page > 1 else None,
            "next_page": f"/api/movies/?page={page + 1}&per_page={page_size}" if page < total_pages else None,
            "total_pages": total_pages,
            "total_items": total_items,
        }

    async def delete_movie(self, movie_id: int):
        return await self.movie_rep.delete(movie_id)

    async def is_admin(self):
        user = await self.user_rep.get_user_from_token()
        return user.has_group(UserGroupEnum.ADMIN)
