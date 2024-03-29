from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class SchedulerMiddleware(BaseMiddleware):
    """
    Middleware for providing a scheduler and cache in a Telegram bot.
    """

    def __init__(self, scheduler: AsyncIOScheduler) -> None:
        """
        Initializes the SchedulerMiddleware with an asynchronous scheduler.

        :param scheduler: Async scheduler for handling tasks.
        """
        self.scheduler = scheduler

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        data["scheduler"] = self.scheduler
        return await handler(event, data)
