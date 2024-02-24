from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_pool(dsn: str, enable_logging: bool = True) -> async_sessionmaker[AsyncSession]:
    """
    Creates and returns an asynchronous database connection pool using SQLAlchemy.

    :param dsn: The database connection string.
    :param enable_logging: Whether to enable SQLAlchemy logging. Default is False.
    :return: An asynchronous session maker configured with the provided database engine.
    """
    engine: AsyncEngine = create_async_engine(url=dsn, echo=enable_logging)
    return async_sessionmaker(engine, expire_on_commit=False)
