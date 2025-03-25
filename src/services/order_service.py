from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserGroupEnum
from database.models.orders import OrderModel
from repositories.accounts_rep import UserRepository
from repositories.cart_item_rep import CartItemRepository
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
            cart_item_repository: CartItemRepository,
            user_repository: UserRepository,

    ):
        self.db = db
        self.order_crud = order_repository
        self.order_item_crud = order_item_repository
        self.cart_crud = cart_repository
        self.cart_item_crud = cart_item_repository
        self.user_crud = user_repository

    async def create_order(self) -> OrderModel:
        try:
            user = await self.user_crud.get_user_from_token()
            user_cart = await self.cart_crud.get_user_cart(user.id)

            cart_items = await self.cart_item_crud.get_all_cart_items_by_cart_id(user_cart.id)

            if not cart_items:
                raise ValueError("Cart is empty")

            movie_ids = [item.movie_id for item in cart_items]

            order = await self.order_crud.create_order(user.id)

            order_items = await self.order_item_crud.create_order_items(order.id, movie_ids)

            total_price = Decimal(sum(item.price_at_order for item in order_items))
            await self.order_crud.update_total_price(order, total_price)

            await self.cart_item_crud.delete_all_cart_items(user_cart.id)

            return order
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_orders(self, user_id: int) -> list[OrderModel]:
        return await self.order_crud.get_orders(user_id)

    async def get_all_orders(self) -> list[OrderModel]:
        return await self.order_crud.get_all_orders()


    async def get_order_with_params(self, **kwargs) -> list[OrderModel]:
        return await self.order_crud.get_orders_with_params(**kwargs)

    async def set_canceled_status(self, order_id: int) -> None:
        await self.order_crud.set_status(order_id, "canceled")

    async def set_paid_status(self, order_id: int) -> None:
        await self.order_crud.set_status(order_id, "paid")

    async def check_user_is_admin(self):
        user = await self.user_crud.get_user_from_token()
        return user.group == UserGroupEnum.ADMIN
