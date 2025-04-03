from typing import List, Optional

from database.models.shopping_cart import CartItemModel, CartModel
from exceptions.cart_item import CartItemNotInCartError
from exceptions.shopping_cart import ShoppingCartNotFoundError
from repositories.accounts_rep import UserRepository
from repositories.cart_item_rep import CartItemRepository
from repositories.shopping_cart_rep import ShoppingCartRepository
from schemas.shopping_cart import (
    CartDetailSchema,
    CartItemDetailSchema,
)


class ShoppingCartService:
    def __init__(
        self,
        shopping_cart_repository: ShoppingCartRepository,
        cart_item_repository: CartItemRepository,
        user_repository: UserRepository,
    ) -> None:
        self.shopping_cart_repository = shopping_cart_repository
        self.cart_item_repository = cart_item_repository
        self.user_repository = user_repository

    async def get_user_cart(
        self,
        create_order_url: Optional[str] = None,
        clear_cart_url: Optional[str] = None,
    ) -> CartDetailSchema:
        user = await self.user_repository.get_user_from_token()

        cart = await self.shopping_cart_repository.get_or_create_cart(user.id)
        items = await self.get_cart_items_details(cart)
        response = CartDetailSchema(
            id=cart.id,
            user_id=user.id,
            create_order_url=create_order_url if items else None,
            clear_cart_url=clear_cart_url if items else None,
            items=items,
        )
        return response

    async def get_cart_by_id(self, cart_id: int) -> CartDetailSchema:
        cart = await self.shopping_cart_repository.get_cart_by_id(cart_id)
        if not cart:
            raise ShoppingCartNotFoundError("Cart not found")
        items = await self.get_cart_items_details(cart)
        response = CartDetailSchema(id=cart.id, user_id=cart.user_id, items=items)
        return response

    async def get_cart_items_details(
        self, cart: CartModel
    ) -> List[CartItemDetailSchema]:
        items = await self.cart_item_repository.get_all_cart_items_by_cart_id(cart.id)

        return (
            [
                CartItemDetailSchema(
                    id=item.id,
                    movie_id=item.movie.id,
                    title=item.movie.name,
                    price=item.movie.price,
                    genres=[genre.name for genre in item.movie.genres],
                    release_year=item.movie.year,
                    warning=(
                        "Movie already purchased. It will be removed from your order"
                        if await self.user_repository.is_movie_in_purchased(
                            cart.user_id, item.movie_id
                        )
                        else None
                    ),
                )
                for item in items
            ]
            if cart
            else []
        )

    async def get_cart_item_detail(
        self, item: CartItemModel, warning: Optional[str]
    ) -> CartItemDetailSchema:
        return CartItemDetailSchema(
            id=item.id,
            movie_id=item.movie.id,
            title=item.movie.name,
            price=item.movie.price,
            genres=[genre.name for genre in item.movie.genres],
            release_year=item.movie.year,
            warning=warning,
        )

    async def get_or_create_cart(self, user_id: int):
        cart = await self.shopping_cart_repository.get_or_create_cart(user_id)
        return cart

    async def add_movie_to_cart(
        self, cart: CartDetailSchema, movie_id
    ) -> CartItemDetailSchema:
        new_item = await self.cart_item_repository.create_cart_item(cart.id, movie_id)
        warning = None
        if await self.user_repository.is_movie_in_purchased(cart.user_id, movie_id):
            warning = "Movie already purchased. It will be removed from your order"
        response = await self.get_cart_item_detail(new_item, warning=warning)
        return response

    async def remove_movie_from_cart(self, cart_id: int, movie_id) -> None:
        cart_item = await (
            self.cart_item_repository.get_cart_item_by_cart_id_and_movie_id(
                cart_id, movie_id
            )
        )

        if not cart_item:
            raise CartItemNotInCartError("Movie not found in cart")

        await self.cart_item_repository.delete_cart_item(cart_item)

    async def clear_cart(self, cart_id: int) -> None:
        await self.cart_item_repository.delete_all_cart_items(cart_id)
