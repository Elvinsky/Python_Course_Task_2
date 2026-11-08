"""Async engine, session factory and the `get_db` FastAPI dependency."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings

settings = get_settings()

# TODO (AC 3): configure connection pooling on this engine: pool_size=10 and max_overflow=20.
# Also consider pool_recycle (seconds) and pool_pre_ping=True.
# See the "connection pooling" section of the README.
engine: AsyncEngine = create_async_engine(settings.database_url, echo=settings.echo_sql)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    """One session per request; `async with` closes it and returns the connection to the pool."""
    async with async_session() as session:
        yield session
