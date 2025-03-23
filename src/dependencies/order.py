from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from repositories.order_item_rep import OrderItemRepository

from repositories.order_rep import OrderRepository


def get_order_repository(
    session: AsyncSession = Depends(get_db),
):
    return OrderRepository(db=session)

def get_order_item_repository(
    session: AsyncSession = Depends(get_db),
):
    return OrderItemRepository(db=session)