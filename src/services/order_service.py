from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.orders import OrderModel
from repositories.order_item_rep import OrderItemRepository
from repositories.order_rep import OrderRepository
from repositories.shopping_cart_rep import ShoppingCartRepository


class OrderService:

    def __init__(
            self,
            db: AsyncSession,
            order_repository: OrderRepository,
            order_item_repository: OrderItemRepository,
            cart_repository: ShoppingCartRepository,
    ):
        self.db = db
        self.order_crud = order_repository
        self.order_item_crud = order_item_repository
        self.cart_crud = cart_repository

    async def create_order(self, user_id: int) -> OrderModel:
        try:
            user_cart = await self.cart_crud.get_user_cart(user_id)

            cart_items = await self.cart_crud.get_items(user_cart)

            movie_ids = [item.movie_id for item in cart_items]

            order = await self.order_crud.create_order(user_id)

            order_items = await self.order_item_crud.create_order_items(order.id, movie_ids)

            total_price = Decimal(sum(item.price_at_order for item in order_items))
            await self.order_crud.update_total_price(order, total_price)

            await self.cart_crud.clear_cart(user_cart)

            return order
        except Exception as e:
            await self.db.rollback()
            raise e
