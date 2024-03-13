from typing import Any, Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.database import RequestsRepo, User
from bot.keyboards import start

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart(), flags={"throttling_key": "default"})
async def process_command_start(
    message: Message, user: User, repo: RequestsRepo, i18n: I18nContext
) -> TelegramMethod[Any]:
    """
    Handler to /start commands with user.

    :param message: The message from Telegram.
    :param user: The database user object.
    :patam repo: The repository for database requests.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    subscriptions: list[str] = await repo.users.get_subscriptions(user=user)
    return message.answer(
        text=i18n.get("start", name=message.from_user.first_name),
        reply_markup=start(subscriptions=subscriptions, i18n=i18n),
    )
