import stripe
from typing import Optional
import logging

from database.models import OrderModel
from src.database.models.payment import Payment, PaymentStatus
from src.repositories.payments_rep import PaymentRepository
from src.schemas.payment import PaymentCreate, PaymentUpdate
#
# logger = logging.getLogger(__name__)
#
# class PaymentService:
#     def __init__(self, payment_repository: PaymentRepository, stripe_secret_key: str):
#         self.payment_repository = payment_repository
#         stripe.api_key = stripe_secret_key
#         self._verify_stripe_connection()
#
#     def _verify_stripe_connection(self):
#         """Перевірка підключення до Stripe API"""
#         try:
#             # Перевіряємо підключення до Stripe API
#             stripe.Balance.retrieve()
#             logger.info("Successfully connected to Stripe API")
#         except stripe.error.APIConnectionError as e:
#             logger.error(f"Failed to connect to Stripe API: {str(e)}")
#             raise Exception("Could not connect to Stripe API. Please check your internet connection and Stripe API key.")
#         except stripe.error.AuthenticationError as e:
#             logger.error(f"Stripe authentication error: {str(e)}")
#             raise Exception("Invalid Stripe API key. Please check your configuration.")
#         except Exception as e:
#             logger.error(f"Unexpected error while connecting to Stripe: {str(e)}")
#             raise Exception("Failed to initialize Stripe connection.")
#
#     async def create_payment_intent(self, payment: PaymentCreate, user_id: int) -> Payment:
#         # Створюємо запис про платіж в базі даних
#         db_payment = await self.payment_repository.create_payment(payment, user_id)
#         logger.info(f"Created payment record with ID: {db_payment.id}")
#
#         try:
#             # Створюємо PaymentIntent в Stripe
#             intent = stripe.PaymentIntent.create(
#                 amount=int(payment.amount * 100),  # Конвертуємо в центи
#                 currency=payment.currency.lower(),
#                 payment_method_types=[payment.payment_method],
#                 metadata={
#                     "payment_id": db_payment.id,
#                     "user_id": user_id
#                 }
#             )
#             logger.info(f"Created Stripe PaymentIntent with ID: {intent.id}")
#
#             # Оновлюємо запис про платіж з transaction_id
#             await self.payment_repository.update_payment(
#                 db_payment.id,
#                 PaymentUpdate(transaction_id=intent.id)
#             )
#             logger.info(f"Updated payment record with transaction_id: {intent.id}")
#
#             return db_payment
#
#         except stripe.error.APIConnectionError as e:
#             logger.error(f"Stripe API connection error: {str(e)}")
#             await self.payment_repository.update_payment(
#                 db_payment.id,
#                 PaymentUpdate(status=PaymentStatus.FAILED)
#             )
#             raise Exception("Failed to connect to Stripe. Please check your internet connection.")
#         except stripe.error.AuthenticationError as e:
#             logger.error(f"Stripe authentication error: {str(e)}")
#             await self.payment_repository.update_payment(
#                 db_payment.id,
#                 PaymentUpdate(status=PaymentStatus.FAILED)
#             )
#             raise Exception("Invalid Stripe API key. Please check your configuration.")
#         except stripe.error.StripeError as e:
#             logger.error(f"Stripe error while creating payment intent: {str(e)}")
#             await self.payment_repository.update_payment(
#                 db_payment.id,
#                 PaymentUpdate(status=PaymentStatus.FAILED)
#             )
#             raise e
#         except Exception as e:
#             logger.error(f"Unexpected error while creating payment: {str(e)}")
#             await self.payment_repository.update_payment(
#                 db_payment.id,
#                 PaymentUpdate(status=PaymentStatus.FAILED)
#             )
#             raise Exception("An unexpected error occurred while processing your payment.")
#
#     async def handle_webhook(self, event: stripe.Event) -> Optional[Payment]:
#         logger.info(f"Processing webhook event: {event.type}")
#
#         if event.type == "payment_intent.succeeded":
#             payment_intent = event.data.object
#             logger.info(f"Payment succeeded for PaymentIntent: {payment_intent.id}")
#
#             payment = await self.payment_repository.get_payment_by_transaction_id(payment_intent.id)
#             if payment:
#                 logger.info(f"Found payment record with ID: {payment.id}")
#                 await self.payment_repository.update_payment(
#                     payment.id,
#                     PaymentUpdate(status=PaymentStatus.COMPLETED)
#                 )
#                 logger.info(f"Updated payment status to COMPLETED")
#                 return payment
#             else:
#                 logger.warning(f"No payment record found for transaction_id: {payment_intent.id}")
#
#         elif event.type == "payment_intent.payment_failed":
#             payment_intent = event.data.object
#             logger.info(f"Payment failed for PaymentIntent: {payment_intent.id}")
#
#             payment = await self.payment_repository.get_payment_by_transaction_id(payment_intent.id)
#             if payment:
#                 logger.info(f"Found payment record with ID: {payment.id}")
#                 await self.payment_repository.update_payment(
#                     payment.id,
#                     PaymentUpdate(status=PaymentStatus.FAILED)
#                 )
#                 logger.info(f"Updated payment status to FAILED")
#                 return payment
#             else:
#                 logger.warning(f"No payment record found for transaction_id: {payment_intent.id}")
#
#         return None
class PaymentService:
    def __init__(self, payment_repository: PaymentRepository, stripe_secret_key: str):
        self.payment_repository = payment_repository
        stripe.api_key = stripe_secret_key

    async def create_payment_session(self, order: OrderModel) -> str:
        session = await self.payment_repository.create_payment_session(order)
        return session.url