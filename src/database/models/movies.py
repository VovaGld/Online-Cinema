from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Column,
    ForeignKey,
    Numeric,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base

MovieGenresModel = Table(
    "movie_genres",
    Base.metadata,
    Column(
        "movie_id",
        ForeignKey("movies.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "genre_id",
        ForeignKey("genres.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)

MovieStarsModel = Table(
    "movie_stars",
    Base.metadata,
    Column(
        "movie_id",
        ForeignKey("movies.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "star_id",
        ForeignKey("stars.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)

MovieDirectorsModel = Table(
    "movie_directors",
    Base.metadata,
    Column(
        "movie_id",
        ForeignKey("movies.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "director_id",
        ForeignKey("directors.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)


class GenreModel(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    movies: Mapped[list["MovieModel"]] = relationship(
        "MovieModel", secondary=MovieGenresModel, back_populates="genres"
    )

    def __repr__(self):
        return f"<Genre(name='{self.name}')>"


class StarModel(Base):
    __tablename__ = "stars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    movies: Mapped[list["MovieModel"]] = relationship(
        "MovieModel", secondary=MovieStarsModel, back_populates="stars"
    )

    def __repr__(self):
        return f"<Star(name='{self.name}')>"


class DirectorModel(Base):
    __tablename__ = "directors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    movies: Mapped[list["MovieModel"]] = relationship(
        "MovieModel", secondary=MovieDirectorsModel, back_populates="directors"
    )

    def __repr__(self):
        return f"<Director(name='{self.name}')>"


class CertificationModel(Base):
    __tablename__ = "certifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    movies: Mapped[list["MovieModel"]] = relationship(back_populates="certification")

    def __repr__(self):
        return f"<Certification(name='{self.name}')>"


class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    movie: Mapped["MovieModel"] = relationship(back_populates="comments")


class MovieModel(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(unique=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    time: Mapped[int] = mapped_column(nullable=False)
    imdb: Mapped[float] = mapped_column(nullable=False)
    votes: Mapped[int] = mapped_column(nullable=False)
    meta_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    gross: Mapped[Optional[float]] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    genres: Mapped[list["GenreModel"]] = relationship(
        "GenreModel", secondary=MovieGenresModel, back_populates="movies"
    )

    stars: Mapped[list["StarModel"]] = relationship(
        "StarModel", secondary=MovieStarsModel, back_populates="movies"
    )

    directors: Mapped[list["DirectorModel"]] = relationship(
        "DirectorModel", secondary=MovieDirectorsModel, back_populates="movies"
    )

    order_items: Mapped[list["OrderItemModel"]] = relationship(
        "OrderItemModel", back_populates="movie"
    )

    comments: Mapped[list["CommentModel"]] = relationship(back_populates="movie")

    certification_id: Mapped[int] = mapped_column(ForeignKey("certifications.id"))
    certification: Mapped["CertificationModel"] = relationship(back_populates="movies")
    likes: Mapped[Optional[int]] = mapped_column(nullable=True, default=0)
    dislikes: Mapped[Optional[int]] = mapped_column(nullable=True, default=0)
    rate: Mapped[Optional[float]] = mapped_column(nullable=True, default=0.0)
    rate_count: Mapped[Optional[int]] = mapped_column(nullable=True, default=0)

    __table_args__ = (
        UniqueConstraint("name", "year", "time", name="unique_movie_constraint"),
    )

    @classmethod
    def default_order_by(cls):
        return [cls.id.desc()]

    def __repr__(self):
        return f"<Movie(name='{self.name}', release_year='{self.year}', duration={self.time})>"
