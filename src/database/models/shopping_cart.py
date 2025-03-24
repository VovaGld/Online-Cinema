from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class CartModel(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user: Mapped["UserModel"] = relationship(back_populates="cart")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    items: Mapped[List["CartItemModel"]] = relationship(
        back_populates="cart", cascade="all, delete-orphan"
    )


class CartItemModel(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    cart: Mapped["CartModel"] = relationship(back_populates="items")
    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id", ondelete="CASCADE"), nullable=False
    )

    movie: Mapped["MovieModel"] = relationship("MovieModel")
    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id", ondelete="CASCADE"), nullable=False
    )

    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("cart_id", "movie_id", name="unique_movie_in_cart_constraint"),
    )
