from typing import List, Optional

import stripe
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from stripe.checkout import Session

from database.models import OrderModel
from src.database.models.payment import Payment, PaymentStatus
from src.schemas.payment import PaymentCreate, PaymentUpdate

class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(self, user_id: int) -> Payment:
        pass

    async def create_payment_session(self, order: OrderModel) -> Session:
        new_session = await stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": f"Order #{order.id}"},
                        "unit_amount": order.total_amount
                    },
                    "quantity": 1
                }
            ],
            mode="payment",
            success_url="google.com",
            cancel_url="youtube.com"
        )

        return new_session