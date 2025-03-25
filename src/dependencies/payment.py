import os

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from repositories.payments_rep import PaymentRepository
from services.payment import PaymentService


def get_payment_repository(
        session: AsyncSession = Depends(get_db)
) -> PaymentRepository:
    return PaymentRepository(session=session)

def get_payment_service(
        payment_repository: PaymentRepository = Depends(get_payment_repository)

) -> PaymentService:
    return PaymentService(
        payment_repository=payment_repository,
        stripe_secret_key=os.getenv("STRIPE_SECRET_KEY")
    )