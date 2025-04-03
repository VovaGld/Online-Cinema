import os

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependencies.order import get_order_repository
from repositories.order_rep import OrderRepository
from repositories.payment_item_rep import PaymentItemRepository
from repositories.payments_rep import PaymentRepository
from services.payment import PaymentService


def get_payment_repository(
    session: AsyncSession = Depends(get_db),
) -> PaymentRepository:
    return PaymentRepository(session=session)


def get_payment_item_repository(
    session: AsyncSession = Depends(get_db),
) -> PaymentItemRepository:
    return PaymentItemRepository(session=session)


def get_payment_service(
    payment_repository: PaymentRepository = Depends(get_payment_repository),
    payment_item_repository: PaymentItemRepository = Depends(
        get_payment_item_repository
    ),
    order_repository: OrderRepository = Depends(get_order_repository),
) -> PaymentService:
    return PaymentService(
        payment_repository=payment_repository,
        payment_item_repository=payment_item_repository,
        order_repository=order_repository,
        stripe_secret_key=os.getenv("STRIPE_SECRET_KEY"),
    )
