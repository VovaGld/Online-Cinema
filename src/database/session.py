import os
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB_PORT = os.getenv("POSTGRES_DB_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

POSTGRESQL_DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_DB_PORT}/{POSTGRES_DB}"
)
postgresql_engine = create_async_engine(POSTGRESQL_DATABASE_URL, echo=False)
AsyncPostgresqlSessionLocal = async_sessionmaker(
    bind=postgresql_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

sync_database_url = POSTGRESQL_DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
sync_postgresql_engine = create_engine(sync_database_url, echo=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session.

    This function returns an async generator yielding a new database session.
    It ensures that the session is properly closed after use.

    :return: An asynchronous generator yielding an AsyncSession instance.
    """
    async with AsyncPostgresqlSessionLocal() as session:
        yield session
