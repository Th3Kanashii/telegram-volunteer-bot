from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware, Bot
from aiogram.types import ForumTopic, Message
from aiogram.utils.markdown import hlink
from aiogram_i18n import I18nContext

from bot.keyboards import builder_reply, start

if TYPE_CHECKING:
    from bot.config import Config
    from bot.services.database import RequestsRepo, Topic, User


class TopicMiddleware(BaseMiddleware):
    """
    Middleware for handling forum topics and user chats in a Telegram bot.
    """

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user: User = data["user"]
        i18n: I18nContext = data["i18n"]
        repo: RequestsRepo = data["repo"]
        config: Config = data["config"]

        active_category: str | None = user.active_category

        if not active_category:
            subscriptions: list[str] = await repo.users.get_subscriptions(user=user)
            return event.answer(
                text=i18n.get("not-category"),
                reply_markup=start(subscriptions=subscriptions, i18n=i18n),
            )

        if active_category == "civic_education":
            return event.answer(
                text=i18n.get("volunteer-not-active"),
                reply_markup=builder_reply(
                    *[i18n.get("cancel-subscribe"), i18n.get("main-menu")],
                    input_field_placeholder=i18n.get("placeholder-write-message"),
                ),
            )

        user_topic = f"{active_category}_topic"
        topic: Topic | None = await repo.topics.get(user_id=user.id)
        if hasattr(topic, user_topic) and not getattr(topic, user_topic):
            bot: Bot = data["bot"]
            chat_id = getattr(config.tg_bot, user.active_category)
            topic_id: ForumTopic = await bot.create_forum_topic(
                chat_id=chat_id, name=event.from_user.first_name
            )
            topic_intro: str = i18n.get(
                "new-topic-intro",
                name=user.name,
                profile=hlink(user.name, event.from_user.url),
                language_code=user.locale,
            )
            await repo.topics.add(
                user_id=user.id, category=active_category, topic_id=topic_id.message_thread_id
            )
            await bot.send_message(
                chat_id=chat_id, text=topic_intro, message_thread_id=topic_id.message_thread_id
            )
            await event.copy_to(chat_id=chat_id, message_thread_id=topic_id.message_thread_id)

            return event.answer(
                text=i18n.get("create-topic"),
                reply_markup=builder_reply(
                    *[i18n.get("cancel-subscribe"), i18n.get("main-menu")],
                    input_field_placeholder=i18n.get("placeholder-write-message"),
                ),
            )

        data["chat_id"] = getattr(config.tg_bot, active_category)
        data["topic_id"] = getattr(topic, user_topic)
        return await handler(event, data)
