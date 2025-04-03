from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.movies import MovieModel
from database.models.orders import OrderItemModel


class OrderItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_movie_by_id(self, movie_id: int) -> Optional[MovieModel]:
        result = await self.db.execute(
            select(MovieModel).where(MovieModel.id == movie_id)
        )
        return result.scalars().first()

    async def create_order_items(
        self, order_id: int, movie_ids: List[int]
    ) -> List[OrderItemModel]:
        try:
            order_items = []
            for movie_id in movie_ids:
                movie = await self.get_movie_by_id(movie_id)
                if not movie:
                    raise ValueError(f"Movie with ID {movie_id} not found")

                order_items.append(
                    OrderItemModel(
                        order_id=order_id, movie_id=movie.id, price_at_order=movie.price
                    )
                )

            self.db.add_all(order_items)
            await self.db.commit()
            return order_items
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e
