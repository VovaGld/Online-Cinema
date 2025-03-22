from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.movies import MovieModel
from database.models.orders import OrderModel, OrderItemModel
from database.models.shopping_cart import CartModel, CartItemModel


async def get_orders(
        user_id: int,
        db: AsyncSession,
) -> list:
    result = await db.execute(select(OrderModel).filter_by(user_id=user_id))
    return result.scalars().all()

async def get_movie_from_card(
        user_id: int,
        db: AsyncSession,
) -> list[MovieModel]:
    result = await db.execute(select(CartModel).where(CartModel.user_id == user_id))
    cart = result.scalars().first()
    result = await db.execute(select(CartItemModel).filter_by(cart_id=cart.id))
    return result.scalars().all()

async def _get_movie_by_id(movie_id: int, db: AsyncSession) -> MovieModel:
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    return result.scalars().first()

async def _create_order_items(
    order_id: int,
    movies: list[CartItemModel],
    db: AsyncSession
) -> list[OrderItemModel]:
    try:
        order_items = []
        for movie in movies:
            movie = await _get_movie_by_id(movie.movie_id, db)
            order_item = OrderItemModel(
                order_id=order_id,
                movie_id=movie.id,
                price_at_order=movie.price
            )
            order_items.append(order_item)

        db.add_all(order_items)
        await db.commit()
        return order_items
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def create_order(
    user_id: int,
    movies: list[MovieModel],
    db: AsyncSession
) -> OrderModel:
    try:
        order = OrderModel(user_id=user_id)
        db.add(order)
        await db.commit()
        await db.refresh(order)

        order_items = []
        for movie in movies:
            result = await db.execute(select(MovieModel).where(MovieModel.id == movie.movie_id))
            fetched_movie = result.scalars().first()

            order_item = OrderItemModel(
                order_id=order.id,
                movie_id=fetched_movie.id,
                price_at_order=fetched_movie.price
            )
            order_items.append(order_item)

        db.add_all(order_items)
        await db.commit()

        total_price = Decimal(sum([item.price_at_order for item in order_items]))

        # Встановлюємо зв'язки вручну.
        order.total_amount = total_price
        await db.commit()
        await db.refresh(order, attribute_names=["order_items", "total_amount"])

        return order
    except SQLAlchemyError:
        await db.rollback()
        raise
