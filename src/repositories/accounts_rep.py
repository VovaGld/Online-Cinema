from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import UserModel, UserGroupEnum
from security.jwt_auth_manager import JWTAuthManager


class UserRepository:
    def __init__(
            self,
            session: AsyncSession,
            JWTmanager: JWTAuthManager,
            token: str
    ):
        self.session = session
        self.jwt_manager = JWTmanager
        self.token = token

    async def get_user_by_id(self, user_id) -> UserModel:
        result = await self.session.execute(
            select(UserModel)
            .options(joinedload(UserModel.group))
            .where(UserModel.id == user_id)
        )
        return result.scalars().first()

    async def get_user_from_token(self) -> UserModel:
        token_info = self.jwt_manager.decode_access_token(self.token)
        return await self.get_user_by_id(token_info["user_id"])

    async def check_user_is_admin(self):
        user = await self.get_user_from_token()
        return user.group.name == UserGroupEnum.ADMIN