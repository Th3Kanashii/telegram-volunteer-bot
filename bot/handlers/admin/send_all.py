import asyncio
from typing import Any, Final

from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.database import RequestsRepo

router: Final[Router] = Router(name=__name__)


@router.message(Command("all", prefix="!"))
async def process_command_send_all(
    message: Message, bot: Bot, repo: RequestsRepo, i18n: I18nContext
) -> TelegramMethod[Any]:
    """
    Handler to command /all
    Send text messages to all users

    :param message: The message from Telegram.
    :param bot: The bot object used to interact with the Telegram API.
    :param repo: The repository for database requests.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    if not message.text or len(message.text) <= 4:
        return message.answer(text=i18n.get("something-went-wrong"))

    users: list[tuple] = await repo.users.get_user_data(("id",))

    for user in users:
        try:
            await bot.send_message(chat_id=user[0], text=f"{message.text[4:]}")
            await asyncio.sleep(0.1)
        except TelegramBadRequest:
            continue

    return message.answer(text=i18n.get("all"))
