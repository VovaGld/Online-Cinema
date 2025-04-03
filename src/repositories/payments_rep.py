from typing import List, Optional

import stripe
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from stripe.checkout import Session

from database.models import OrderModel
from database.models.payment import PaymentModel, PaymentStatus


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_payment_by_session_id(
        self, session_id: str
    ) -> Optional[PaymentModel]:
        result = await self.session.execute(
            select(PaymentModel).where(PaymentModel.session_id == session_id)
        )
        return result.scalars().first()

    async def get_payments(self, user_id: int) -> List[PaymentModel]:
        result = await self.session.execute(
            select(PaymentModel).filter_by(user_id=user_id)
        )
        return result.scalars().all()

    async def get_all_payments(self) -> List[PaymentModel]:
        result = await self.session.execute(select(PaymentModel))
        return result.scalars().all()

    async def get_payments_with_params(self, **kwargs) -> List[PaymentModel]:
        query = select(PaymentModel)
        if kwargs.get("status"):
            query = query.filter_by(status=kwargs["status"])
        if kwargs.get("user_id"):
            query = query.filter_by(user_id=kwargs["user_id"])
        if kwargs.get("date_payment"):
            query = query.filter(
                func.date(PaymentModel.created_at) == kwargs["date_order"]
            )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_payment(
        self, user_id: int, order: OrderModel, payment_session: Session
    ) -> PaymentModel:
        try:
            new_payment = PaymentModel(
                user_id=user_id,
                order_id=order.id,
                amount=order.total_amount,
                session_id=payment_session.id,
                session_url=payment_session.url,
            )
            self.session.add(new_payment)
            await self.session.commit()
            await self.session.refresh(new_payment)
            return new_payment
        except stripe.error.StripeError as e:
            raise e

    def create_payment_session(
        self, order: OrderModel, success_url, cancel_url
    ) -> Session:
        success_url = success_url + "?session_id={CHECKOUT_SESSION_ID}"
        cancel_url = cancel_url + "?session_id={CHECKOUT_SESSION_ID}"

        new_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": f"Order #{order.id}"},
                        "unit_amount": int(order.total_amount * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )

        return new_session

    async def set_status(self, session_id: str, status: str):
        payment = await self.get_payment_by_session_id(session_id)
        if status == "paid":
            payment.status = PaymentStatus.COMPLETED
        elif status == "failed":
            payment.status = PaymentStatus.FAILED
        elif status == "canceled":
            payment.status = PaymentStatus.CANCELLED
        await self.session.commit()
