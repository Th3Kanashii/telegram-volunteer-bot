from typing import Any, Final

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext

from bot.keyboards import builder_inline

router: Final[Router] = Router(name=__name__)


@router.message(Command("language"))
async def process_choose_a_language(message: Message, i18n: I18nContext) -> Any:
    """
    Handler user subscription to specific categories.

    :param message: The message from Telegram.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    return message.answer(
        text=i18n.get("choose-a-language"),
        reply_markup=builder_inline(width=3, language_en="🇬🇧", language_uk="🇺🇦", language_ja="🇯🇵"),
    )


@router.callback_query(F.data.startswith("language"))
async def process_set_the_language(callback: CallbackQuery, i18n: I18nContext) -> Any:
    """
    Handler admin callback for change language.

    :param callback: The callback query from the admin.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    await i18n.set_locale(callback.data.split("_")[1])
    return callback.message.edit_text(text=i18n.get("admin-language"))
