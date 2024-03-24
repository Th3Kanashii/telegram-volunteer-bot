from typing import Any, Final

from aiogram import Router
from aiogram.filters import JOIN_TRANSITION, ChatMemberUpdatedFilter
from aiogram.methods import TelegramMethod
from aiogram.types import ChatMemberUpdated
from aiogram.utils.markdown import hlink
from aiogram_i18n import I18nContext

from bot.filters import JoinGroup

new_member_router: Final[Router] = Router(name=__name__)


@new_member_router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION), JoinGroup())
async def process_new_member(event: ChatMemberUpdated, i18n: I18nContext) -> TelegramMethod[Any]:
    """
    Handles new chat members and sends a welcome message.

    :param event: Triggered when a member joins the chat.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    return event.answer(
        i18n.get("new-member", name=hlink(event.from_user.first_name, event.from_user.url))
    )
