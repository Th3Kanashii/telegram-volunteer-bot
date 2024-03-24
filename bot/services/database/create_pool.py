from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_pool(dsn: str) -> async_sessionmaker[AsyncSession]:
    """
    Creates and returns an asynchronous database connection pool using SQLAlchemy.

    :param dsn: The database connection string.
    :return: An asynchronous session maker configured with the provided database engine.
    """
    engine: AsyncEngine = create_async_engine(url=dsn, echo=False)
    return async_sessionmaker(engine, expire_on_commit=False)
