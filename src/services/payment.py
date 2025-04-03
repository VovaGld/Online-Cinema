import stripe

from database.models import OrderModel, PaymentModel
from repositories.order_rep import OrderRepository
from repositories.payment_item_rep import PaymentItemRepository
from repositories.payments_rep import PaymentRepository


class PaymentService:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        payment_item_repository: PaymentItemRepository,
        order_repository: OrderRepository,
        stripe_secret_key: str,
    ):
        self.payment_repository = payment_repository
        self.payment_item_repository = payment_item_repository
        self.order_repository = order_repository
        stripe.api_key = stripe_secret_key

    async def create_payment_session(
        self, order: OrderModel, success_url: str, cancel_url: str
    ) -> str:
        payment_session = self.payment_repository.create_payment_session(
            order=order, success_url=success_url, cancel_url=cancel_url
        )
        payment = await self.payment_repository.create_payment(
            order=order, user_id=1, payment_session=payment_session
        )
        order_items = await self.order_repository.get_order_items(order.id)
        payment.order_items = order_items.order_items
        await self.payment_item_repository.create_payment_items(
            payment.id, order_items.order_items
        )
        return payment_session.url

    async def get_payments(self, user_id: int) -> list[PaymentModel]:
        return await self.payment_repository.get_payments(user_id)

    async def get_all_payments(self) -> list[PaymentModel]:
        return await self.payment_repository.get_all_payments()

    async def get_payments_with_params(self, **kwargs) -> list[PaymentModel]:
        return await self.payment_repository.get_payments_with_params(**kwargs)

    async def set_paid_status(self, session_id: str):
        await self.payment_repository.set_status(session_id, "paid")

    async def set_failed_status(self, session_id: str):
        await self.payment_repository.set_status(session_id, "failed")

    async def set_canceled_status(self, session_id: str):
        await self.payment_repository.set_status(session_id, "canceled")
