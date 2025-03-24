from typing import List

from fastapi import HTTPException, status

from database.models.shopping_cart import CartItemModel, CartModel
from repositories.shopping_cart_rep import ShoppingCartRepository
from repositories.cart_item_rep import CartItemRepository
from schemas.shopping_cart import (
    CartDetailSchema,
    CartItemDetailSchema,
)
from security.interfaces import JWTAuthManagerInterface
from exceptions.cart_item import CartItemNotInCartError


class ShoppingCartService:
    def __init__(
        self,
        shopping_cart_repository: ShoppingCartRepository,
        cart_item_repository: CartItemRepository,
    ) -> None:
        self.shopping_cart_repository = shopping_cart_repository
        self.cart_item_repository = cart_item_repository

    async def get_user_cart(self, token: str, jwt_manager: JWTAuthManagerInterface) -> CartDetailSchema:
        try:
            payload = jwt_manager.decode_access_token(token)
            user_id = payload.get("user_id")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )

        cart = await self.shopping_cart_repository.get_or_create_cart(user_id)
        items = await self.get_cart_items_details(cart)
        response = CartDetailSchema(
            id=cart.id,
            user_id=user_id,
            items=items
        )
        return response

    async def get_cart_items_details(self, cart: CartModel) -> List[CartItemDetailSchema]:
        items = await self.cart_item_repository.get_all_cart_items_by_cart_id(cart.id)

        return [
            CartItemDetailSchema(
                id=item.id,
                movie_id=item.movie.id,
                title=item.movie.name,
                price=item.movie.price,
                genres=[genre.name for genre in item.movie.genres],
                release_year=item.movie.year,
                warning=None,
            )
            for item in items
        ] if cart else []

    async def get_cart_item_detail(self, item: CartItemModel) -> CartItemDetailSchema:
        return CartItemDetailSchema(
                id=item.id,
                movie_id=item.movie.id,
                title=item.movie.name,
                price=item.movie.price,
                genres=[genre.name for genre in item.movie.genres],
                release_year=item.movie.year,
                warning=None,
            )

    async def get_or_create_cart(self, user_id: int):
        cart = await self.shopping_cart_repository.get_or_create_cart(user_id)
        return cart

    async def add_movie_to_cart(self, cart_id: int, movie_id) -> CartItemDetailSchema:
        new_item = await self.cart_item_repository.create_cart_item(cart_id, movie_id)

        response = await self.get_cart_item_detail(new_item)
        return response

    async def remove_movie_from_cart(self, cart_id: int, movie_id) -> None:
        cart_item = await (
            self
            .cart_item_repository
            .get_cart_item_by_cart_id_and_movie_id(
                cart_id, movie_id
            )
        )

        if not cart_item:
            raise CartItemNotInCartError("Movie not found in cart")

        await self.cart_item_repository.delete_cart_item(cart_item)

    async def clear_cart(self, cart_id: int) -> None:
        await self.cart_item_repository.delete_all_cart_items(cart_id)
