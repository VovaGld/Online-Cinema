from typing import List

from fastapi import HTTPException, status

from database.models.shopping_cart import CartItemModel, CartModel
from repositories.shopping_cart_rep import ShoppingCartRepository
from repositories.cart_item_rep import CartItemRepository
from schemas.shopping_cart import (
    CartResponseSchema,
    CartItemDetailSchema,
)
from security.interfaces import JWTAuthManagerInterface


class ShoppingCartService:
    def __init__(
        self,
        shopping_cart_repository: ShoppingCartRepository,
        cart_item_repository: CartItemRepository,
    ) -> None:
        self.shopping_cart_repository = shopping_cart_repository
        self.cart_item_repository = cart_item_repository

    async def get_user_cart(self, token: str, jwt_manager: JWTAuthManagerInterface) -> CartResponseSchema:
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
        response = CartResponseSchema(
            user_id=user_id,
            items=items
        )
        return response

    async def get_cart_items_details(self, cart: CartModel) -> List[CartItemDetailSchema]:
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
            for item in cart.items
        ] if cart else []

    async def get_or_create_cart(self, user_id: int):
        cart = await self.shopping_cart_repository.get_or_create_cart(user_id)
        return cart

    async def add_movie_to_cart(self, cart_id: int, movie_id) -> CartItemModel:
        new_item = await self.cart_item_repository.create_cart_item(cart_id, movie_id)
        return new_item

    async def clear_cart(self, cart_id: int) -> None:
        await self.cart_item_repository.delete_all_cart_items(cart_id)
