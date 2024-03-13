from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.database import RequestsRepo


class DatabaseMiddleware(BaseMiddleware):
    """
    Middleware for database sessions and data manipulation repository.
    """

    session_pool: async_sessionmaker[AsyncSession]

    __slots__ = ("session_pool",)

    def __init__(self, session_pool: async_sessionmaker[AsyncSession]) -> None:
        """
        Initializes with async_sessionmaker for database sessions.

        :param session_pool: Async database session manager.
        """
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        session: AsyncSession
        async with self.session_pool() as session:
            data["repo"] = RequestsRepo(session)
            return await handler(event, data)
