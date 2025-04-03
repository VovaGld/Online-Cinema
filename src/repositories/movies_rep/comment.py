from sqlalchemy.ext.asyncio import AsyncSession

from database.models import CommentModel
from schemas.movie import CommentCreateSchema


class CommentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, movie_id: int, user_id: int, comment: CommentCreateSchema):
        db_comment = CommentModel(user_id=user_id, movie_id=movie_id, text=comment.text)
        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)

        return db_comment
