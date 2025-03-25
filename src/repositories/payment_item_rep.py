from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import OrderItemModel, PaymentItemModel, MovieModel


class PaymentItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment_items(self, payment_id: int, order_items: list[OrderItemModel]) -> None:
        print("Order Items:", order_items)
        try:
            payment_items = []
            for item in order_items:
                print(item)
                payment_items.append(
                    PaymentItemModel(
                        payment_id=payment_id,
                        order_item_id=item.id,
                        price_at_payment=item.price_at_order
                    )
                )

            self.session.add_all(payment_items)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
