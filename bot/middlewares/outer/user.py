from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import Chat, Message, user

if TYPE_CHECKING:
    from bot.services.database import RequestsRepo, User


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
        aiogram_user: User | None = await repo.users.get(user_id=tg_user.id)
        if aiogram_user is None:
            aiogram_user = await repo.users.add(tg_user=tg_user)
            data["commands"] = True

        data["user"] = aiogram_user
        return await handler(event, data)
