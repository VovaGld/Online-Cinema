from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.orders import OrderModel, OrderStatus


class OrderRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_orders(self, user_id: int) -> List[OrderModel]:
        result = await self.db.execute(select(OrderModel).filter_by(user_id=user_id))
        return result.scalars().all()

    async def get_order_by_id(self, order_id: int) -> Optional[OrderModel]:
        result = await self.db.execute(select(OrderModel).filter_by(id=order_id))
        return result.scalars().first()

    async def create_order(self, user_id: int) -> OrderModel:
        try:
            order = OrderModel(user_id=user_id)
            self.db.add(order)
            await self.db.commit()
            await self.db.refresh(order)
            return order
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def update_total_price(self, order: OrderModel, total_price):
        try:
            order.total_amount = total_price
            await self.db.commit()
            await self.db.refresh(order, attribute_names=["total_amount"])
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def set_status(self, order_id: int, status: str) -> None:
        order = await self.get_order_by_id(order_id)
        if status == "canceled":
            order.status = OrderStatus.CANCELED
        elif status == "paid":
            order.status = OrderStatus.PAID
        await self.db.commit()
        await self.db.refresh(order)
