from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, Bot
from aiogram.methods import TelegramMethod
from aiogram.types import ForumTopic, Message
from aiogram.utils.markdown import hlink
from aiogram_i18n import I18nContext

from bot.config import Config
from bot.database import RequestsRepo, User
from bot.keyboards import builder_reply, start


class TopicMiddleware(BaseMiddleware):
    """
    Middleware for handling forum topics and user chats in a Telegram bot.
    """

    @staticmethod
    async def create_topic(
        event: Message, bot: Bot, chat_id: int, user: User, repo: RequestsRepo, i18n: I18nContext
    ) -> TelegramMethod[Any]:
        """
        Create a new forum topic and associated chat for a user.

        :param event: The message from Telegram.
        :param bot: The bot object used to interact with the Telegram API.
        :param chat_id: The chat ID where the topic and chat will be created.
        :param user: The database user object.
        :param repo: The repository for database requests.
        :param i18n: The internationalization context for language localization.
        :return: The Telegram method to create a new forum topic.
        """
        topic_id: ForumTopic = await bot.create_forum_topic(
            chat_id=chat_id, name=event.from_user.first_name
        )
        topic_intro: str = i18n.get(
            "new-topic-intro",
            name=event.from_user.first_name,
            profile=hlink(event.from_user.first_name, event.from_user.url),
            username=event.from_user.username,
            language_code=event.from_user.language_code,
        )
        await bot.send_message(
            chat_id=chat_id, text=topic_intro, message_thread_id=topic_id.message_thread_id
        )
        await repo.users.add_topic_id(user=user, topic_id=topic_id.message_thread_id)
        await event.copy_to(chat_id=chat_id, message_thread_id=topic_id.message_thread_id)
        return event.answer(
            text=i18n.get("create-topic"),
            reply_markup=builder_reply(
                *[i18n.get("cancel-subscribe"), i18n.get("main-menu")],
                input_field_placeholder=i18n.get("placeholder-write-message"),
            ),
        )

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        bot: Bot = data["bot"]
        user: User = data["user"]
        i18n: I18nContext = data["i18n"]
        repo: RequestsRepo = data["repo"]
        config: Config = data["config"]

        active_category: str | None = user.active_category
        user_topic = f"{active_category}_topic"

        if not active_category:
            subscriptions: list[str] = await repo.users.get_subscriptions(user=user)
            return event.answer(
                text=i18n.get("not-category"),
                reply_markup=start(subscriptions=subscriptions, i18n=i18n),
            )

        if hasattr(user, user_topic) and not getattr(user, user_topic):
            chat_id = getattr(config.tg_bot, user.active_category)
            return await self.create_topic(
                event=event, bot=bot, chat_id=chat_id, user=user, repo=repo, i18n=i18n
            )

        if active_category == "civic_education":
            return event.answer(
                text=i18n.get("volunteer-not-active"),
                reply_markup=builder_reply(
                    *[i18n.get("cancel-subscribe"), i18n.get("main-menu")],
                    input_field_placeholder=i18n.get("placeholder-write-message"),
                ),
            )

        data["chat_id"] = getattr(config.tg_bot, active_category)
        data["topic_id"] = getattr(user, user_topic)
        return await handler(event, data)
