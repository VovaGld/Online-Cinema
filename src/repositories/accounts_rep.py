from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import UserGroupEnum, UserModel, UserPurchasedMoviesModel
from security.jwt_auth_manager import JWTAuthManager


class UserRepository:
    def __init__(self, session: AsyncSession, JWTmanager: JWTAuthManager, token: str):
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

    async def is_movie_in_purchased(self, user_id: int, movie_id: int) -> bool:
        query = select(UserPurchasedMoviesModel).where(
            and_(
                UserPurchasedMoviesModel.c.user_id == user_id,
                UserPurchasedMoviesModel.c.movie_id == movie_id,
            )
        )
        result = await self.session.execute(query)
        return True if result.scalar() else False

    async def add_movie_to_purchased(self, user_id: int, movie_id: int) -> None:
        existing_purchase = await self.is_movie_in_purchased(user_id, movie_id)
        if not existing_purchase:
            stmt = insert(UserPurchasedMoviesModel).values(
                user_id=user_id, movie_id=movie_id
            )
            await self.session.execute(stmt)
            await self.session.commit()
