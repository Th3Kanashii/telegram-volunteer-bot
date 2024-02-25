from typing import Any, Final

from aiogram import Router
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext

router: Final[Router] = Router(name=__name__)


@router.message(Command("help"), flags={"throttling_key": "default"})
async def process_command_help(message: Message, i18n: I18nContext) -> TelegramMethod[Any]:
    """
    Handler to /help commands.
    Send a message with the help information.

    :param message: The message from Telegram.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    return message.answer(i18n.get("help-user", name=message.from_user.first_name))
