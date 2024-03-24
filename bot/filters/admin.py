from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.filters import Filter
from aiogram.types import Message

if TYPE_CHECKING:
    from bot.config import Config


class Admin(Filter):
    """
    A filter class for Telegram messages to check,
    If the user sending the message is an admin.
    """

    def __init__(self, command: bool = True) -> None:
        """
        Initialize the Admin filter.

        :param command: Apply the filter to command messages only.
        """
        self.command = command

    async def __call__(self, message: Message, config: Config) -> bool:
        """
        Check if the user is an admin in a valid chat.

        :param message: The message from Telegram.
        :param config: The configuration object from the loaded configuration.
        :return: True if the conditions for being an admin are met, False otherwise.
        """
        is_admin: bool = message.from_user.id in config.tg_bot.admins
        is_admin_chat: bool = message.chat.id in config.tg_bot.all_groups
        is_topic: bool = message.message_thread_id is None

        if self.command:
            return is_admin and is_admin_chat and is_topic

        return is_admin and is_admin_chat and not is_topic
