from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.orders import OrderItemModel
from database.models.movies import MovieModel


class OrderItemRepository:

    table_user_movie = []

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_movie_by_id(self, movie_id: int) -> Optional[MovieModel]:
        result = await self.db.execute(select(MovieModel).where(MovieModel.id == movie_id))
        return result.scalars().first()

    async def create_order_items(self, order_id: int, movie_ids: List[int]) -> List[OrderItemModel]:
        try:
            order_items = []
            for movie_id in movie_ids:
                movie = await self.get_movie_by_id(movie_id)
                if not movie:
                    raise ValueError(f"Movie with ID {movie_id} not found")

                if await self.check_movie_buy(movie_id):
                    raise ValueError("You have already bought this movie")

                order_items.append(
                    OrderItemModel(
                        order_id=order_id,
                        movie_id=movie.id,
                        price_at_order=movie.price
                    )
                )

            self.db.add_all(order_items)
            await self.db.commit()
            return order_items
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def check_movie_buy(self, movie_id) -> bool:
        return movie_id in self.table_user_movie
