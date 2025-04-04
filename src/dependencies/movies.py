from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependencies.accounts import get_user_repository
from repositories.accounts_rep import UserRepository
from repositories.movies_rep.certification import CertificationRepository
from repositories.movies_rep.director import DirectorRepository
from repositories.movies_rep.genre import GenreRepository
from repositories.movies_rep.movie import MovieRepository
from repositories.movies_rep.star import StarRepository
from repositories.movies_rep.comment import CommentRepository
from services.movie_service.certification import CertificationService
from services.movie_service.director import DirectorService
from services.movie_service.genre import GenreService
from services.movie_service.movie import MovieService
from services.movie_service.star import StarService
from services.movie_service.comment import CommentService


def _get_genre_repository(
    session: AsyncSession = Depends(get_db),
):
    return GenreRepository(db=session)


def _get_star_repository(
    session: AsyncSession = Depends(get_db),
):
    return StarRepository(db=session)


def _get_director_repository(
    session: AsyncSession = Depends(get_db),
):
    return DirectorRepository(db=session)


def _get_certification_repository(
    session: AsyncSession = Depends(get_db),
):
    return CertificationRepository(db=session)


def _get_movie_repository(
    session: AsyncSession = Depends(get_db),
):
    return MovieRepository(db=session)


def _get_comment_repository(
    session: AsyncSession = Depends(get_db),
):
    return CommentRepository(db=session)


def get_genre_service(
    genre_repository: GenreRepository = Depends(_get_genre_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> GenreService:
    return GenreService(
        genre_rep=genre_repository,
        user_rep=user_repository,
    )


def get_star_service(
    star_repository: StarRepository = Depends(_get_star_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> StarService:
    return StarService(
        star_rep=star_repository,
        user_rep=user_repository,
    )


def get_director_service(
    director_repository: DirectorRepository = Depends(_get_director_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> DirectorService:
    return DirectorService(
        director_rep=director_repository,
        user_rep=user_repository,
    )


def get_certification_service(
    certification_repository: CertificationRepository = Depends(
        _get_certification_repository
    ),
    user_repository: UserRepository = Depends(get_user_repository),
) -> CertificationService:
    return CertificationService(
        certification_rep=certification_repository,
        user_rep=user_repository,
    )


def get_movie_service(
    movie_repository: MovieRepository = Depends(_get_movie_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    db: AsyncSession = Depends(get_db),
) -> MovieService:
    return MovieService(movie_rep=movie_repository, user_rep=user_repository, db=db)

  
def get_comment_service(
    comment_repository: CommentRepository = Depends(_get_comment_repository),
    user_repository: UserRepository = Depends(get_user_repository),
    db: AsyncSession = Depends(get_db),
) -> CommentService:
    return CommentService(
        comment_rep=comment_repository, user_rep=user_repository, db=db
    )
