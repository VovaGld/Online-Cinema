from database.models.shopping_cart import CartItemModel
from repositories.shopping_cart_rep import ShoppingCartRepository
from repositories.cart_item_rep import CartItemRepository


class ShoppingCartService:
    def __init__(
        self,
        shopping_cart_repository: ShoppingCartRepository,
        cart_item_repository: CartItemRepository,
    ) -> None:
        self.shopping_cart_repository = shopping_cart_repository
        self.cart_item_repository = cart_item_repository

    async def get_or_create_cart(self, user_id: int):
        cart = await self.shopping_cart_repository.get_or_create_cart(user_id)
        return cart

    async def add_movie_to_cart(self, cart_id: int, movie_id) -> CartItemModel:
        new_item = await self.cart_item_repository.create_cart_item(cart_id, movie_id)
        return new_item

    async def clear_cart(self, cart_id: int) -> None:
        await self.cart_item_repository.delete_all_cart_items(cart_id)
