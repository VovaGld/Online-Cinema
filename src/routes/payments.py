from fastapi import APIRouter, Depends, HTTPException, Request, Header, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import os
import stripe
import logging
import json

from database.session import get_db
from repositories.payments_rep import PaymentRepository
from schemas.payment import PaymentCreate, PaymentResponse
from services.payment import PaymentService
from security.jwt_auth_manager import JWTAuthManager
from exceptions import InvalidTokenError, TokenExpiredError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: AsyncSession = Depends(get_db),
        jwt_manager: JWTAuthManager = Depends(),
):
    token = credentials.credentials

    try:
        payload = jwt_manager.decode_access_token(token)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: user_id missing")

        return {"id": user_id}
    except TokenExpiredError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/", response_model=PaymentResponse)
async def create_payment(
        payment: PaymentCreate,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    payment_repository = PaymentRepository(db)
    payment_service = PaymentService(payment_repository, stripe_secret_key=os.getenv('STRIPE_SECRET_KEY'))

    try:
        return await payment_service.create_payment_intent(payment, current_user["id"])
    except stripe.error.APIConnectionError as e:
        logger.error(f"Stripe API connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment service is temporarily unavailable. Please try again later."
        )
    except stripe.error.AuthenticationError as e:
        logger.error(f"Stripe authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Payment service configuration error. Please contact support."
        )
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[PaymentResponse])
async def get_user_payments(
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    payment_repository = PaymentRepository(db)
    return await payment_repository.get_user_payments(current_user["id"])


@router.post("/webhook")
async def stripe_webhook(
        request: Request,
        stripe_signature: Optional[str] = Header(None),
        db: AsyncSession = Depends(get_db)
):
    payload = await request.body()
    sig_header = stripe_signature or request.headers.get("stripe-signature")

    logger.info(f"Received webhook with signature: {sig_header}")

    # Для тестування через Swagger UI
    if not sig_header:
        try:
            # Спробуємо обробити payload як звичайний JSON
            event_data = json.loads(payload)
            logger.info(f"Processing test webhook with event type: {event_data.get('type')}")

            payment_repository = PaymentRepository(db)
            payment_service = PaymentService(payment_repository, stripe_secret_key=os.getenv('STRIPE_SECRET_KEY'))

            # Створюємо тестовий event
            event = stripe.Event.construct_from(event_data, stripe.api_key)
            payment = await payment_service.handle_webhook(event)
            return {"status": "success", "payment": payment}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON payload"
            )
        except Exception as e:
            logger.error(f"Error processing test webhook: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    # Для реальних вебхуків від Stripe
    payment_repository = PaymentRepository(db)
    payment_service = PaymentService(payment_repository, stripe_secret_key=os.getenv('STRIPE_SECRET_KEY'))

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv('STRIPE_WEBHOOK_SECRET')
        )
        logger.info(f"Successfully verified webhook signature for event type: {event.type}")
        payment = await payment_service.handle_webhook(event)
        return {"status": "success", "payment": payment}
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature"
        )
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/success")
async def payment_success():
    return {"status": "success", "message": "Payment completed successfully"}


@router.get("/cancel")
async def payment_cancel():
    return {"status": "cancelled", "message": "Payment was cancelled"}
