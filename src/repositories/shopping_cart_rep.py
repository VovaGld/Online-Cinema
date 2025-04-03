from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import MovieModel
from database.models.shopping_cart import CartItemModel, CartModel
from exceptions.shopping_cart import CreateShoppingCartError


class ShoppingCartRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_or_create_cart(self, user_id: int) -> CartModel:
        cart = await self.get_user_cart(user_id)
        if not cart:
            cart = await self.create_cart(user_id)
        return cart

    async def create_cart(self, user_id: int) -> CartModel:
        try:
            cart = CartModel(user_id=user_id)
            self._session.add(cart)
            await self._session.commit()
            await self._session.refresh(cart)
        except SQLAlchemyError as exception:
            await self._session.rollback()
            raise CreateShoppingCartError(str(exception))
        return cart

    async def get_user_cart(self, user_id: int) -> Optional[CartModel]:
        result = await self._session.execute(
            select(CartModel)
            .options(
                selectinload(CartModel.items)
                .joinedload(CartItemModel.movie)
                .selectinload(MovieModel.genres)
            )
            .filter(CartModel.user_id == user_id)
        )
        cart = result.scalars().first()
        return cart if cart else None

    async def get_cart_by_id(self, cart_id: int) -> Optional[CartModel]:
        result = await self._session.execute(
            select(CartModel)
            .options(
                selectinload(CartModel.items)
                .joinedload(CartItemModel.movie)
                .selectinload(MovieModel.genres)
            )
            .filter(CartModel.id == cart_id)
        )
        cart = result.scalars().first()
        return cart if cart else None
