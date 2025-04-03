from datetime import date

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import RedirectResponse
from typing_extensions import Optional

from database.models.orders import OrderStatus
from dependencies.order import get_order_service
from dependencies.payment import get_payment_service
from schemas.movie import BaseResponseSchema
from schemas.order import OrderListSchema, OrderSchema
from services.order_service import OrderService
from services.payment import PaymentService

router = APIRouter()


@router.post("/create/", status_code=301, response_model=None)
async def create(
    order: OrderService = Depends(get_order_service),
    payment: PaymentService = Depends(get_payment_service),
    request: Request = Request,
):
    try:
        order_ = await order.create_order()
        success_payment_url = str(request.url_for("payment_success"))
        cancel_payment_url = str(request.url_for("payment_cancel"))
        payment_url = await payment.create_payment_session(
            order=order_, success_url=success_payment_url, cancel_url=cancel_payment_url
        )

    except SQLAlchemyError as e:
        raise e
    return RedirectResponse(url=payment_url)


@router.get("/list/", response_model=None)
async def get_orders(
    request: Request = Request,
    order: OrderService = Depends(get_order_service),
    user_id: Optional[int] = Query(None),
    status: Optional[OrderStatus] = Query(None),
    date_order: Optional[date] = Query(None),
):
    if await order.user_crud.check_user_is_admin():
        if user_id or status or date_order:
            orders = await order.get_order_with_params(
                user_id=user_id, status=status, date_order=date_order
            )
        else:
            orders = await order.get_all_orders()
    else:
        user = await order.user_crud.get_user_from_token()
        orders = await order.get_orders(user.id)

    result = []
    for order_ in orders:
        movies = await order.get_movies_from_orders(order_.id)
        movie_responses = [
            BaseResponseSchema(id=movie["id"], name=movie["name"]) for movie in movies
        ]
        result.append(
            OrderSchema(
                datetime=order_.created_at,
                movies=movie_responses,
                total_price=order_.total_amount,
                status=order_.status,
                cancel_url=str(request.url_for("cancel_order", order_id=order_.id))
                if order_.status == OrderStatus.PENDING
                else None,
            )
        )
    return OrderListSchema(orders=result)


@router.post("/cancel/{order_id}", response_model=None)
async def cancel_order(order_id: int, order: OrderService = Depends(get_order_service)):
    await order.set_canceled_status(order_id)
    return {"message": "Order cancelled"}
