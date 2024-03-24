from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.filters import Filter
from aiogram.types import Message

if TYPE_CHECKING:
    from bot.config import Config


class SuperAdmin(Filter):
    """
    A filter class for Telegram messages to check,
    If the user sending the message is a super admin.
    """

    async def __call__(self, message: Message, config: Config) -> bool:
        """
        Check if the user is a super admin in a valid chat.

        :param message: The message from Telegram.
        :param config: The configuration object from the loaded configuration.
        :return: True if the conditions for being a super admin are met, False otherwise.
        """
        is_super_admin: bool = message.from_user.id == config.tg_bot.super_admin
        is_super_chat: bool = message.chat.id == config.tg_bot.civic_education

        return is_super_admin and is_super_chat
