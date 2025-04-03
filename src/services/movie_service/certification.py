from database import UserGroupEnum
from repositories.accounts_rep import UserRepository
from repositories.movies_rep.certification import CertificationRepository
from schemas.movie import BaseCreateSchema


class CertificationService:
    def __init__(
        self, certification_rep: CertificationRepository, user_rep: UserRepository
    ) -> None:
        self.certification_rep = certification_rep
        self.user_rep = user_rep

    async def create_certification(self, certification: BaseCreateSchema):
        return await self.certification_rep.create(certification)

    async def get_certification(self, certification_id: int):
        return await self.certification_rep.get(certification_id)

    async def get_all_certifications(self):
        return await self.certification_rep.get_all()

    async def delete_certification(self, certification_id: int):
        return await self.certification_rep.delete(certification_id)

    async def is_admin(self):
        user = await self.user_rep.get_user_from_token()
        return user.has_group(UserGroupEnum.ADMIN)
