from datetime import date

from fastapi import APIRouter, Depends, Request, Query, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing_extensions import Optional

from database.models.orders import OrderStatus
from dependencies.order import get_order_service
from dependencies.payment import get_payment_service
from schemas.order import OrderCreateResponseSchema, OrderListSchema
from security.http import get_token
from services.order_service import OrderService
from services.payment import PaymentService

router = APIRouter()


@router.post("/create/")
async def create(
        order: OrderService = Depends(get_order_service),
        payment: PaymentService = Depends(get_payment_service),
        request: Request = Request
) -> OrderCreateResponseSchema:
    try:
        order = await order.create_order()
        success_payment_url = str(request.url_for("payment_success"))
        cancel_payment_url = str(request.url_for("payment_cancel"))
        payment_url = payment.create_payment_session(order=order, success_url=success_payment_url, cancel_url=cancel_payment_url)

        cancel_url = request.url_for("cancel_order", order_id=order.id)
    except SQLAlchemyError as e:
        raise e
    return OrderCreateResponseSchema(
        order_id=order.id,
        total_price=order.total_amount,
        status=order.status,
        payment_url=payment_url,
        cancel_url=str(cancel_url)
    )


@router.get("/list/", response_model=OrderListSchema)
async def get_orders(
        order: OrderService = Depends(get_order_service),
        user_id: Optional[int] = Query(None),
        status: Optional[OrderStatus] = Query(None),
        date_order: Optional[date] = Query(None)
) -> OrderListSchema:
    if await order.user_crud.check_user_is_admin():
        if user_id or status or date_order:
            orders = await order.get_order_with_params(
                user_id=user_id,
                status=status,
                date_order=date_order
            )
        else:
            orders = await order.get_all_orders()
    else:
        user = await order.user_crud.get_user_from_token()
        orders = await order.get_orders(user.id)

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


@router.get("/success/")
async def payment_success(
    session_id: Optional[str] = Query(None)
):
    print(session_id)
    return {"status": "success", "message": "Payment completed successfully"}


@router.get("/cancel/")
async def payment_cancel(
    session_id: Optional[str] = Query(None),
):
    if session_id:
        print(session_id)
    else:
        raise HTTPException(
            status_code=400,
            detail="Payment ID is required"
        )
    return {"status": "success", "message": "Payment completed successfully"}
