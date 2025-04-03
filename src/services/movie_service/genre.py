from database import UserGroupEnum
from repositories.accounts_rep import UserRepository
from repositories.movies_rep.genre import GenreRepository
from schemas.movie import BaseCreateSchema


class GenreService:
    def __init__(self, genre_rep: GenreRepository, user_rep: UserRepository) -> None:
        self.genre_rep = genre_rep
        self.user_rep = user_rep

    async def create_genre(self, genre: BaseCreateSchema):
        return await self.genre_rep.create(genre)

    async def get_genre(self, genre_id: int):
        return await self.genre_rep.get(genre_id)

    async def get_all_genres(self):
        return await self.genre_rep.get_all()

    async def delete_genre(self, genre_id: int):
        return await self.genre_rep.delete(genre_id)

    async def is_admin(self):
        user = await self.user_rep.get_user_from_token()
        return user.has_group(UserGroupEnum.ADMIN)
