from typing import Optional

import stripe
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from stripe.checkout import Session

from database.models import OrderModel
from src.database.models.payment import Payment, PaymentStatus

class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        result = await self.session.execute(select(Payment).where(Payment.id == payment_id))
        return result.scalars().first()

    async def create_payment(self, user_id: int) -> Payment:
        pass


    def create_payment_session(self, order: OrderModel, success_url, cancel_url) -> Session:
        success_url = success_url + "?session_id={CHECKOUT_SESSION_ID}"
        cancel_url = cancel_url + "?session_id={CHECKOUT_SESSION_ID}"

        new_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": f"Order #{order.id}"},
                        "unit_amount": int(order.total_amount * 100)
                    },
                    "quantity": 1
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url
        )

        return new_session

    async def set_status(self, payment_id, status: str):
        payment = await self.get_payment_by_id(payment_id)
        if status == "paid":
            payment.status = PaymentStatus.COMPLETED
        elif status == "failed":
            payment.status = PaymentStatus.FAILED
        elif status == "canceled":
            payment.status = PaymentStatus.CANCELLED
        await self.session.commit()