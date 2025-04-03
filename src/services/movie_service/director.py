from database import UserGroupEnum
from repositories.accounts_rep import UserRepository
from repositories.movies_rep.director import DirectorRepository
from schemas.movie import BaseCreateSchema


class DirectorService:
    def __init__(
        self, director_rep: DirectorRepository, user_rep: UserRepository
    ) -> None:
        self.director_rep = director_rep
        self.user_rep = user_rep

    async def create_director(self, director: BaseCreateSchema):
        return await self.director_rep.create(director)

    async def get_director(self, director_id: int):
        return await self.director_rep.get(director_id)

    async def get_all_directors(self):
        return await self.director_rep.get_all()

    async def delete_director(self, director_id: int):
        return await self.director_rep.delete(director_id)

    async def is_admin(self):
        user = await self.user_rep.get_user_from_token()
        return user.has_group(UserGroupEnum.ADMIN)
