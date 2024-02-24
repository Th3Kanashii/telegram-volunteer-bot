from typing import Any

from aiogram.types import ChatMemberMember, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from bot.config import Config


def builder_inline(width: int = 2, **kwargs: Any) -> InlineKeyboardMarkup:
    """
    Build an InlineKeyboardMarkup with a single row of InlineKeyboardButtons.

    :param width: The number of buttons to display in a row, defaults to 2.
    :return: InlineKeyboardMarkup containing a single row of InlineKeyboardButtons.
    """
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    builder.row(
        *[
            InlineKeyboardButton(text=text, callback_data=callback_data)
            for callback_data, text in kwargs.items()
        ],
        width=width,
    )
    return builder.as_markup()


def living_library(
    member: ChatMemberMember, i18n: I18nContext, config: Config
) -> InlineKeyboardMarkup:
    """
    Generates an inline keyboard with a subscription link.

    :param member: The object ChatMemberMember.
    :param i18n: The internationalization context for language localization.
    :param config: The configuration object from the loaded configuration.
    :return: Inline keyboard markup with a button to subscribe.
    """
    if isinstance(member, ChatMemberMember):
        text = i18n.get("living-library-sub")
    else:
        text = i18n.get("living-library-not-sub")

    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text=text, url=config.tg_bot.living_library_url))
    return keyboard.as_markup()
