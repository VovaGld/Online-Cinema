from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from repositories.shopping_cart_rep import ShoppingCartRepository


def get_shopping_cart_repository(
    session: AsyncSession = Depends(get_db),
) -> ShoppingCartRepository:
    return ShoppingCartRepository(session=session)
