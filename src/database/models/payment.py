import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PaymentModel(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))

    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus), default=PaymentStatus.PENDING
    )
    session_id: Mapped[str] = mapped_column(unique=True)
    session_url: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="payments")
    order: Mapped["OrderModel"] = relationship("OrderModel", back_populates="payments")
    payment_items: Mapped[list["PaymentItemModel"]] = relationship(
        "PaymentItemModel", back_populates="payment", cascade="all, delete-orphan"
    )


class PaymentItemModel(Base):
    __tablename__ = "payment_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    payment_id: Mapped[int] = mapped_column(ForeignKey("payments.id"))
    payment: Mapped["PaymentModel"] = relationship(
        "PaymentModel", back_populates="payment_items"
    )
    order_item_id: Mapped[int] = mapped_column(ForeignKey("order_items.id"))
    order_item: Mapped["OrderItemModel"] = relationship(
        "OrderItemModel", back_populates="payment_items"
    )
    price_at_payment: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True)
