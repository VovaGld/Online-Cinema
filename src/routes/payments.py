from typing import Optional

from fastapi import APIRouter, Query
from fastapi.params import Depends

from dependencies.order import get_order_service
from dependencies.payment import get_payment_service
from services.order_service import OrderService
from services.payment import PaymentService

router = APIRouter()


@router.get("/success/")
async def payment_success(
        payment: PaymentService = Depends(get_payment_service),
        order: OrderService = Depends(get_order_service),
        session_id: Optional[str] = Query(None)
):
    await payment.set_paid_status(session_id)
    payment_ = await payment.payment_repository.get_payment_by_session_id(session_id)
    await order.set_paid_status(payment_.order_id)
    await order.add_order_to_purchased(payment_.order_id)
    return {"status": "success", "message": "Payment completed successfully"}


@router.get("/cancel/")
async def payment_cancel(
        payment: PaymentService = Depends(get_payment_service),
        order: OrderService = Depends(get_order_service),
        session_id: Optional[str] = Query(None)
):
    await payment.set_canceled_status(session_id)
    payment_ = await payment.payment_repository.get_payment_by_session_id(session_id)
    await order.set_canceled_status(payment_.order_id)
    return {"status": "success", "message": "Payment completed successfully"}
