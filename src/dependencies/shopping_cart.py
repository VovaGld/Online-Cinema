from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from repositories.cart_item_rep import CartItemRepository
from repositories.shopping_cart_rep import ShoppingCartRepository
from services.shopping_cart import ShoppingCartService


def get_shopping_cart_repository(
    session: AsyncSession = Depends(get_db),
) -> ShoppingCartRepository:
    return ShoppingCartRepository(session=session)

def get_shopping_cart_item_repository(
    session: AsyncSession = Depends(get_db),
) -> CartItemRepository:
    return CartItemRepository(session=session)

def get_shopping_cart_service(
    shopping_cart_repository = Depends(get_shopping_cart_repository),
    cart_item_repository = Depends(get_shopping_cart_item_repository),
) -> ShoppingCartService:
    return ShoppingCartService(
        shopping_cart_repository=shopping_cart_repository,
        cart_item_repository=cart_item_repository,
    )
