from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from aiogram_i18n import I18nContext
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware for throttling message processing based on specified limits.
    """

    def __init__(self, limit: int | float = 0.5) -> None:
        """
        Initializes ThrottlingMiddleware with a specified throttling limit.

        :param limit: Throttling limit in seconds. Default is 0.5 seconds.
        """
        super().__init__()
        self.cache: dict[str, TTLCache] = {"default": TTLCache(maxsize=100, ttl=limit)}

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        i18n: I18nContext = data["i18n"]
        throttling_key = get_flag(data, "throttling_key")

        if throttling_key is not None and throttling_key in self.cache:
            if event.chat.id in self.cache[throttling_key]:
                return event.answer(text=i18n.get("something-went-wrong"))
            self.cache[throttling_key][event.chat.id] = None
        return await handler(event, data)
