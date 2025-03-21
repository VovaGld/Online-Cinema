from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base
from database.models.movies import MovieModel
from database.models.accounts import UserModel

class CartModel(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user: Mapped["UserModel"] = relationship("User", back_populates="cart")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
