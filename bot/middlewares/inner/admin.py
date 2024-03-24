from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

if TYPE_CHECKING:
    from bot.config import Config
    from bot.services.database import RequestsRepo


class AdminMiddleware(BaseMiddleware):
    """
    Middleware for extracting user ID and category from message thread and chat
    """

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        repo: RequestsRepo = data["repo"]
        config: Config = data["config"]
        categories: dict[int, tuple[str, str]] = {
            config.tg_bot.youth_policy: ("youth_policy", "Youth policy 📚"),
            config.tg_bot.legal_support: ("legal_support", "Legal support ⚖️"),
            config.tg_bot.psychologist_support: ("psychologist_support", "Psychologist support 🧘"),
        }
        category_values = categories.get(event.chat.id)
        category, category_label = category_values

        user_id: int = await repo.topics.get_user_id(
            topic_id=event.message_thread_id,
            category=category,
        )

        data["user_id"] = user_id
        data["category"] = category_label
        return await handler(event, data)
