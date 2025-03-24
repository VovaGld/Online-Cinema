from fastapi import APIRouter, Depends, Request
from sqlalchemy.exc import SQLAlchemyError

from dependencies.order import get_order_service
from schemas.order import OrderCreateResponseSchema, OrderListSchema
from services.order_service import OrderService

router = APIRouter()


@router.post("/create/")
async def create(
        order: OrderService = Depends(get_order_service),
        request: Request = Request
) -> OrderCreateResponseSchema:
    try:
        order = await order.create_order(user_id=2)
        cancel_url = request.url_for("cancel_order", order_id=order.id)
    except SQLAlchemyError as e:
        raise e
    return OrderCreateResponseSchema(
        order_id=order.id,
        total_price=order.total_amount,
        status=order.status,
        payment_url="some url",
        cancel_url=str(cancel_url)
    )


@router.get("/list/", response_model=OrderListSchema)
async def get_orders(
        order: OrderService = Depends(get_order_service)
) -> OrderListSchema:
    orders = await order.get_orders(user_id=2)
    result = [
        OrderCreateResponseSchema(
            order_id=order.id,
            total_price=order.total_amount,
            status=order.status,
            payment_url="some url",
        ) for order in orders
    ]
    return OrderListSchema(orders=result)


@router.post("/cancel/{order_id}")
async def cancel_order(
        order_id: int,
        order: OrderService = Depends(get_order_service)
):
    await order.set_canceled_status(order_id)
    return {"message": "Order cancelled"}

