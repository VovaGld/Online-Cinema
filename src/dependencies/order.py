from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from repositories.order_item_rep import OrderItemRepository

from repositories.order_rep import OrderRepository
from services.order_service import OrderService
from dependencies.shopping_cart import ShoppingCartRepository as Cart, get_shopping_cart_repository


def _get_order_repository(
    session: AsyncSession = Depends(get_db),
):
    return OrderRepository(db=session)

def _get_order_item_repository(
    session: AsyncSession = Depends(get_db),
):
    return OrderItemRepository(db=session)

def get_order_service(
    order_repository: OrderRepository = Depends(_get_order_repository),
    order_item_repository: OrderItemRepository = Depends(_get_order_item_repository),
    cart_repository: Cart = Depends(get_shopping_cart_repository),
    db: AsyncSession = Depends(get_db)
) -> OrderService:
    return OrderService(
        db=db,
        order_repository=order_repository,
        order_item_repository=order_item_repository,
        cart_repository=cart_repository
    )