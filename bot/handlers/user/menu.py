from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Bot, Router
from aiogram.filters import Command, CommandStart
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.keyboards import builder_reply, start
from bot.middlewares import ThrottlingMiddleware

from ..ui_commands import set_user_commands

if TYPE_CHECKING:
    from bot.services.database import RequestsRepo, User

menu_router: Final[Router] = Router(name=__name__)
menu_router.message.middleware(ThrottlingMiddleware(limit=1))


@menu_router.message(CommandStart(), flags={"throttling_key": "default"})
async def start_command(
    message: Message,
    bot: Bot,
    user: User,
    repo: RequestsRepo,
    i18n: I18nContext,
    commands: bool | None = False,
) -> TelegramMethod[Any]:
    """
    Handler to /start commands with user.

    :param message: The message from Telegram.
    :param user: The database user object.
    :patam repo: The repository for database requests.
    :param i18n: The internationalization context for language localization.
    :param commands: A flag to set user commands.
    :return: A Telegram method.
    """
    if commands:
        await set_user_commands(bot=bot, i18n=i18n, chat_id=user.id)

    subscriptions: list[str] = await repo.users.get_subscriptions(user=user)
    return message.answer(
        text=i18n.get("start", name=message.from_user.first_name),
        reply_markup=start(subscriptions=subscriptions, i18n=i18n),
    )


@menu_router.message(Command("help"), flags={"throttling_key": "default"})
async def help_command(message: Message, i18n: I18nContext) -> TelegramMethod[Any]:
    """
    Handler to /help commands.
    Send a message with the help information.

    :param message: The message from Telegram.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    return message.answer(i18n.get("help-user", name=message.from_user.first_name))


@menu_router.message(Command("language"), flags={"throttling_key": "default"})
async def language_command(message: Message, i18n: I18nContext) -> TelegramMethod[Any]:
    """
    Handler to /language commands.

    :param message: The message from Telegram.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    return message.answer(
        text=i18n.get("choose-a-language"),
        reply_markup=builder_reply(
            *["EN 🇬🇧", "UA 🇺🇦", "JA 🇯🇵"],
            input_field_placeholder=i18n.get("placeholder-language"),
            width=2,
        ),
    )
