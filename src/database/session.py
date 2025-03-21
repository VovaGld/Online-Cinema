from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

BASE_DIR = Path(__file__).parent.parent
PATH_TO_DB = str(BASE_DIR / "database" / "cinema.db")

SQLITE_DATABASE_URL = f"sqlite+aiosqlite:///{PATH_TO_DB}"
sqlite_engine = create_async_engine(SQLITE_DATABASE_URL, echo=False)
AsyncSQLiteSessionLocal = sessionmaker(  # type: ignore
    bind=sqlite_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSQLiteSessionLocal() as session:
        yield session