from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Chat, Message, user

from bot.database import RequestsRepo, User


class UserMiddleware(BaseMiddleware):
    """
    Middleware for handling user information in a Telegram bot.
    """

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        tg_user: user.User = data.get("event_from_user")
        chat: Chat | None = data.get("event_chat")
        if tg_user is None or chat is None or tg_user.is_bot:
            return await handler(event, data)

        repo: RequestsRepo = data["repo"]
        aiogram_user: User | None = await repo.users.get_user(user_id=tg_user.id)
        if aiogram_user is None:
            data["user"] = await repo.users.add_user(tg_user=tg_user)
            return await handler(event, data)

        data["user"] = aiogram_user
        return await handler(event, data)
