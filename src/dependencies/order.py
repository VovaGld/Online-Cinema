from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from dependencies.accounts import get_user_repository
from dependencies.shopping_cart import (
    get_shopping_cart_item_repository,
    get_shopping_cart_repository,
)
from repositories.accounts_rep import UserRepository
from repositories.cart_item_rep import CartItemRepository
from repositories.order_item_rep import OrderItemRepository
from repositories.order_rep import OrderRepository
from repositories.shopping_cart_rep import ShoppingCartRepository
from services.order_service import OrderService


from dependencies.shopping_cart import (
    ShoppingCartRepository as Cart,
    get_shopping_cart_repository,
    get_shopping_cart_item_repository,
)


def get_order_repository(
    session: AsyncSession = Depends(get_db),
):
    return OrderRepository(db=session)


def get_order_item_repository(
    session: AsyncSession = Depends(get_db),
):
    return OrderItemRepository(db=session)


def get_order_service(
    order_repository: OrderRepository = Depends(get_order_repository),
    order_item_repository: OrderItemRepository = Depends(get_order_item_repository),
    cart_repository: ShoppingCartRepository = Depends(get_shopping_cart_repository),
    cart_item_repository: CartItemRepository = Depends(
        get_shopping_cart_item_repository
    ),
    user_repository: UserRepository = Depends(get_user_repository),
    db: AsyncSession = Depends(get_db),
) -> OrderService:
    return OrderService(
        db=db,
        order_repository=order_repository,
        order_item_repository=order_item_repository,
        cart_repository=cart_repository,
        user_repository=user_repository,
        cart_item_repository=cart_item_repository,
    )
