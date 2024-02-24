from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.database import RequestsRepo, User
from bot.keyboards import builder_reply, start

router: Final[Router] = Router(name=__name__)


@router.message(Command("language"), flags={"throttling_key": "default"})
async def process_choose_a_language(message: Message, i18n: I18nContext) -> Any:
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
            width=3,
        ),
    )


@router.message(F.text.in_(["EN 🇬🇧", "UA 🇺🇦", "JA 🇯🇵"]))
async def process_set_the_language(
    message: Message, user: User, i18n: I18nContext, repo: RequestsRepo
) -> Any:
    """
    Handler for processing language selection in the Telegram bot.

    :param message: The message from Telegram.
    :param user: The database user object.
    :param i18n: The internationalization context for language localization.
    :param repo: The repository for database requests.
    :return: A Telegram method.
    """
    subscriptions: list[str] = await repo.users.get_user_subscriptions(user=user)
    await i18n.set_locale(message.text.split()[0].lower() if message.text != "UA 🇺🇦" else "uk")
    return message.answer(
        text=i18n.get("start", name=message.from_user.first_name),
        reply_markup=start(subscriptions=subscriptions, i18n=i18n),
    )
