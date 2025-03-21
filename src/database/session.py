from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from database.models.base import Base


BASE_DIR = Path(__file__).parent.parent
PATH_TO_DB = str(BASE_DIR / "database" / "cinema.db")

SQLITE_DATABASE_URL = f"sqlite+aiosqlite:///{PATH_TO_DB}"
sqlite_engine = create_async_engine(SQLITE_DATABASE_URL, echo=False)
AsyncSQLiteSessionLocal = async_sessionmaker(
    bind=sqlite_engine,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSQLiteSessionLocal() as session:
        yield session


async def init_db() -> None:
    """
    Initialize the database.

    This function creates all tables defined in the SQLAlchemy ORM models.
    It should be called at the application startup to ensure that the database schema exists.
    """
    from database.models import accounts, movies


    async with sqlite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close the database connection.

    This function disposes of the database engine, releasing all associated resources.
    It should be called when the application shuts down to properly close the connection pool.
    """
    await sqlite_engine.dispose()
