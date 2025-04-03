from datetime import date
from typing import Optional

from fastapi import APIRouter, Query
from fastapi.params import Depends

from database.models.payment import PaymentStatus
from dependencies.accounts import get_email_notificator, get_user_repository
from dependencies.order import get_order_service
from dependencies.payment import get_payment_service
from notifications import EmailSender
from repositories.accounts_rep import UserRepository
from schemas.payment import PaymentListSchema, PaymentSchema
from services.order_service import OrderService
from services.payment import PaymentService

router = APIRouter()


@router.get("/success/")
async def payment_success(
    payment: PaymentService = Depends(get_payment_service),
    order: OrderService = Depends(get_order_service),
    email: EmailSender = Depends(get_email_notificator),
    user: UserRepository = Depends(get_user_repository),
    session_id: Optional[str] = Query(None),
):
    await payment.set_paid_status(session_id)
    payment_ = await payment.payment_repository.get_payment_by_session_id(session_id)
    await order.set_paid_status(payment_.order_id)
    await order.add_order_to_purchased(payment_.order_id)
    user_ = await user.get_user_from_token()
    await email.send_payment_complete_email(email=user_.email, payment=payment_)
    return {"status": "success", "message": "Payment completed successfully"}


@router.get("/cancel/")
async def payment_cancel(
    payment: PaymentService = Depends(get_payment_service),
    order: OrderService = Depends(get_order_service),
    session_id: Optional[str] = Query(None),
):
    await payment.set_canceled_status(session_id)
    payment_ = await payment.payment_repository.get_payment_by_session_id(session_id)
    await order.set_canceled_status(payment_.order_id)
    return {"status": "success", "message": "Payment completed successfully"}


@router.get("/list/", response_model=None)
async def get_payments(
    user: UserRepository = Depends(get_user_repository),
    payment: PaymentService = Depends(get_payment_service),
    user_id: Optional[int] = Query(None),
    status: Optional[PaymentStatus] = Query(None),
    date_payment: Optional[date] = Query(None),
):
    if await user.check_user_is_admin():
        if user_id or status or date_payment:
            payments = await payment.get_payments_with_params(
                user_id=user_id, status=status, date_order=date_payment
            )
        else:
            payments = await payment.get_all_payments()
    else:
        user = await user.get_user_from_token()
        payments = await payment.get_payments(user.id)

    result = [
        PaymentSchema(
            datetime=payment_.created_at,
            amount=payment_.amount,
            status=payment_.status,
            payment_url=payment_.session_url
            if payment_.status != PaymentStatus.COMPLETED
            else None,
        )
        for payment_ in payments
    ]
    return PaymentListSchema(payments=result)
