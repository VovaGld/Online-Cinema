from datetime import datetime
from decimal import Decimal
from sqlalchemy import Integer, ForeignKey, DateTime, Enum, DECIMAL, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from enum import Enum as PyEnum

from database.models.base import Base
from database.models.accounts import UserModel


class OrderStatus(PyEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELED = "canceled"


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="orders")
    order_items: Mapped[list["OrderItemModel"]] = relationship("OrderItemModel", back_populates="order", cascade="all, delete-orphan")


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    price_at_order: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    order: Mapped["OrderModel"] = relationship("OrderModel", back_populates="order_items")
    movie: Mapped["MovieModel"] = relationship("MovieModel")