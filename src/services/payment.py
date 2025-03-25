import stripe

from database.models import OrderModel
from src.repositories.payments_rep import PaymentRepository

class PaymentService:
    def __init__(self, payment_repository: PaymentRepository, stripe_secret_key: str):
        self.payment_repository = payment_repository
        stripe.api_key = stripe_secret_key

    def create_payment_session(
            self,
            order: OrderModel,
            success_url: str,
            cancel_url: str
    ) -> str:
        session = self.payment_repository.create_payment_session(order, cancel_url=cancel_url, success_url=success_url)
        return session.url

    async def set_paid_status(self, payment_id: int):
        await self.payment_repository.set_status(payment_id, "paid")

    async def set_failed_status(self, payment_id: int):
        await self.payment_repository.set_status(payment_id, "failed")

    async def set_canceled_status(self, payment_id: int):
        await self.payment_repository.set_status(payment_id, "canceled")