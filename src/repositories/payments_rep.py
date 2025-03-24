from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models.payment import Payment, PaymentStatus
from src.schemas.payment import PaymentCreate, PaymentUpdate

class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, payment: PaymentCreate, user_id: int) -> Payment:
        db_payment = Payment(
            **payment.model_dump(),
            user_id=user_id
        )
        self.db.add(db_payment)
        await self.db.commit()
        await self.db.refresh(db_payment)
        return db_payment

    async def get_payment(self, payment_id: int) -> Optional[Payment]:
        query = select(Payment).where(Payment.id == payment_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_payment_by_transaction_id(self, transaction_id: str) -> Optional[Payment]:
        query = select(Payment).where(Payment.transaction_id == transaction_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_payments(self, user_id: int) -> List[Payment]:
        query = select(Payment).where(Payment.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_payment(self, payment_id: int, payment_update: PaymentUpdate) -> Optional[Payment]:
        db_payment = await self.get_payment(payment_id)
        if not db_payment:
            return None

        update_data = payment_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_payment, field, value)

        await self.db.commit()
        await self.db.refresh(db_payment)
        return db_payment

    async def get_pending_payments(self) -> List[Payment]:
        query = select(Payment).where(Payment.status == PaymentStatus.PENDING)
        result = await self.db.execute(query)
        return list(result.scalars().all())
