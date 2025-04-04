from typing import Optional, Sequence

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models.movies import MovieModel
from database.models.shopping_cart import CartItemModel
from exceptions.cart_item import (
    AddCartItemError,
    CartItemAlreadyInCartError,
    DeleteCartItemError,
)


class CartItemRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_cart_item_by_id(self, cart_item_id: int):
        result = await self._session.execute(
            select(CartItemModel).filter(CartItemModel.id == cart_item_id)
        )
        return result.scalars().first()

    async def get_cart_item_by_cart_id_and_movie_id(
        self, cart_id: int, movie_id: int
    ) -> Optional[CartItemModel]:
        result = await self._session.execute(
            select(CartItemModel).filter(
                CartItemModel.cart_id == cart_id, CartItemModel.movie_id == movie_id
            )
        )
        return result.scalars().first()

    async def get_all_cart_items_by_cart_id(
        self, cart_id: int
    ) -> Sequence[CartItemModel]:
        result = await self._session.execute(
            select(CartItemModel)
            .options(joinedload(CartItemModel.movie).joinedload(MovieModel.genres))
            .filter(CartItemModel.cart_id == cart_id)
        )

        return result.unique().scalars().all()

    async def create_cart_item(self, cart_id: int, movie_id: int) -> CartItemModel:
        existing_item = await self.get_cart_item_by_cart_id_and_movie_id(
            cart_id, movie_id
        )
        if existing_item:
            raise CartItemAlreadyInCartError("Movie is already in the cart")
        try:
            cart_item = CartItemModel(cart_id=cart_id, movie_id=movie_id)
            self._session.add(cart_item)
            await self._session.commit()
            await self._session.refresh(cart_item)
        except SQLAlchemyError as exception:
            await self._session.rollback()
            raise AddCartItemError(str(exception))

        result = await self._session.execute(
            select(CartItemModel)
            .options(joinedload(CartItemModel.movie).joinedload(MovieModel.genres))
            .filter(CartItemModel.id == cart_item.id)
        )
        return result.scalars().first()

    async def delete_cart_item(self, cart_item: CartItemModel) -> None:
        try:
            await self._session.delete(cart_item)
            await self._session.commit()
        except SQLAlchemyError as exception:
            await self._session.rollback()
            raise DeleteCartItemError(str(exception))

    async def delete_all_cart_items(self, cart_id: int) -> None:
        await self._session.execute(
            delete(CartItemModel).where(CartItemModel.cart_id == cart_id)
        )
        await self._session.commit()
