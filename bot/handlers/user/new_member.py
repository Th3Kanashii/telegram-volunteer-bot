from typing import Any, Final

from aiogram import Router
from aiogram.filters import JOIN_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from aiogram.utils.markdown import hlink
from aiogram_i18n import I18nContext

router: Final[Router] = Router(name=__name__)


@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def new_member(event: ChatMemberUpdated, i18n: I18nContext) -> Any:
    """
    Handles new chat members and sends a welcome message.

    :param event: Triggered when a member joins the chat.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    return event.answer(
        i18n.get("new-member", name=hlink(event.from_user.first_name, event.from_user.url))
    )
