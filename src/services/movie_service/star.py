from database import UserGroupEnum
from repositories.accounts_rep import UserRepository
from repositories.movies_rep.star import StarRepository
from schemas.movie import BaseCreateSchema


class StarService:
    def __init__(self, star_rep: StarRepository, user_rep: UserRepository) -> None:
        self.star_rep = star_rep
        self.user_rep = user_rep

    async def create_star(self, star: BaseCreateSchema):
        return await self.star_rep.create(star)

    async def get_star(self, star_id: int):
        return await self.star_rep.get(star_id)

    async def get_all_stars(self):
        return await self.star_rep.get_all()

    async def delete_star(self, star_id: int):
        return await self.star_rep.delete(star_id)

    async def is_admin(self):
        user = await self.user_rep.get_user_from_token()
        return user.has_group(UserGroupEnum.ADMIN)
