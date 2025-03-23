from typing import List, Optional

from sqlalchemy import select, Sequence, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from database.models.accounts import UserModel
from database.models.movies import MovieModel
from database.models.shopping_cart import CartModel, CartItemModel
from exceptions.shopping_cart import (
    CreateShoppingCartError,
    CartItemAlreadyInCartError,
    AddCartItemError,
    DeleteCartItemError,
)


class ShoppingCartRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_or_create_cart(self, user: UserModel) -> CartModel:
        cart = await self.get_user_cart(user.id)
        if not cart:
            cart = await self.create_cart(user)
        return cart

    async def create_cart(self, user: UserModel) -> CartModel:
        try:
            async with self._session.begin():
                cart = CartModel(user_id=user.id)
                self._session.add(cart)
                await self._session.flush()
                await self._session.refresh(cart)
        except SQLAlchemyError as exception:
            await self._session.rollback()
            print(f"SQLAlchemy error: {exception}")
            raise CreateShoppingCartError(str(exception))
        return cart

    async def get_user_cart(self, user_id: int) -> Optional[CartModel]:
        result = await self._session.execute(
            select(CartModel)
            .options(selectinload(CartModel.items).joinedload(CartItemModel.movie))
            .filter(CartModel.user_id == user_id)
        )
        cart = result.scalars().first()
        return cart if cart else None

    async def get_item(self, cart: CartModel, cart_item_id: int):
        result = await self._session.execute(
            select(CartItemModel)
            .filter(CartItemModel.cart_id == cart.id, CartItemModel.id == cart_item_id)
        )
        return result.scalars().first()

    async def get_item_by_movie_id(self, cart: CartModel, movie_id: int) -> Optional[CartItemModel]:
        result = await self._session.execute(
            select(CartItemModel)
            .filter(CartItemModel.cart_id == cart.id, CartItemModel.movie_id == movie_id)
        )
        return result.scalars().first()

    async def get_items(self, cart: CartModel) -> Sequence[CartItemModel]:
        result = await self._session.execute(
            select(CartItemModel)
            .options(joinedload(CartItemModel.movie).joinedload(MovieModel.genres))
            .filter(CartItemModel.cart_id == cart.id)
        )

        return result.unique().scalars().all()

    async def create_item(self, cart: CartModel, movie: MovieModel) -> CartItemModel:
        existing_item = self.get_item_by_movie_id(cart, movie.id)
        if existing_item:
            raise CartItemAlreadyInCartError(
                "Movie is already in the cart"
            )
        try:
            async with self._session.begin():
                cart_item = CartItemModel(cart_id=cart.id, movie_id=movie.id)
                self._session.add(cart_item)
                await self._session.flush()
                await self._session.refresh(cart_item)
        except SQLAlchemyError as exception:
            await self._session.rollback()
            print(f"SQLAlchemy error: {exception}")
            raise AddCartItemError(str(exception))
        return cart_item

    async def delete_item(self, cart_item: CartItemModel) -> None:
        try:
            async with self._session.begin():
                await self._session.delete(cart_item)
        except SQLAlchemyError as exception:
            await self._session.rollback()
            print(f"SQLAlchemy error: {exception}")
            raise DeleteCartItemError(str(exception))

    async def clear_cart(self, cart: CartModel) -> None:
        try:
            async with self._session.begin():
                await self._session.execute(
                    delete(CartItemModel).where(CartItemModel.cart_id == cart.id)
                )
        except SQLAlchemyError as exception:
            await self._session.rollback()
            print(f"SQLAlchemy error: {exception}")
            raise DeleteCartItemError(str(exception))
