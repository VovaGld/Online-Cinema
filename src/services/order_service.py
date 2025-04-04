from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.orders import OrderModel
from repositories.accounts_rep import UserRepository
from repositories.cart_item_rep import CartItemRepository
from repositories.movies_rep.movie import MovieRepository
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
        self.movie_repository = MovieRepository(db)

    async def create_order(self) -> OrderModel:
        try:
            user = await self.user_crud.get_user_from_token()
            user_cart = await self.cart_crud.get_user_cart(user.id)

            if not user_cart:
                raise HTTPException(status_code=400, detail="No movies in cart")

            cart_items = await self.cart_item_crud.get_all_cart_items_by_cart_id(
                user_cart.id
            )

            movie_ids = [
                item.movie_id
                for item in cart_items
                if not await self.user_crud.is_movie_in_purchased(
                    user_id=user.id, movie_id=item.movie_id
                )
            ]

            if not movie_ids:
                raise HTTPException(status_code=400, detail="No movies in cart")

            try:
                order = await self.order_crud.create_order(user.id)
            except SQLAlchemyError as e:
                raise HTTPException(status_code=400, detail=str(e))

            try:
                order_items = await self.order_item_crud.create_order_items(
                    order.id, movie_ids
                )
            except SQLAlchemyError as e:
                raise HTTPException(status_code=400, detail=str(e))

            order.order_items = order_items

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

    async def get_movies_from_orders(self, order_id: int) -> list[dict]:
        movie_list = []
        order_items = await self.order_crud.get_order_items(order_id)
        for item in order_items.order_items:
            movie_list.append(await self.movie_repository.get(item.movie_id))
        return [{"id": movie.id, "name": movie.name} for movie in movie_list]

    async def set_canceled_status(self, order_id: int) -> None:
        await self.order_crud.set_status(order_id, "canceled")

    async def set_paid_status(self, order_id: int) -> None:
        await self.order_crud.set_status(order_id, "paid")

    async def add_order_to_purchased(self, order_id: int) -> None:
        user = await self.user_crud.get_user_from_token()
        order_items = await self.order_crud.get_order_items(order_id)
        for order_item in order_items.order_items:
            await self.user_crud.add_movie_to_purchased(user.id, order_item.movie_id)
