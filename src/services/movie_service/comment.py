from sqlalchemy.ext.asyncio import AsyncSession

from repositories.accounts_rep import UserRepository
from repositories.movies_rep.comment import CommentRepository
from schemas.movie import CommentCreateSchema


class CommentService:
    def __init__(
        self, comment_rep: CommentRepository, user_rep: UserRepository, db: AsyncSession
    ) -> None:
        self.comment_rep = comment_rep
        self.user_rep = user_rep
        self.db = db

    async def create_comment(self, movie_id: int, comment: CommentCreateSchema):
        user = await self.user_rep.get_user_from_token()

        return await self.comment_rep.create(
            movie_id=movie_id, comment=comment, user_id=user.id
        )
