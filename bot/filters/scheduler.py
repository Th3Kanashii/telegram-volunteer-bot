from aiogram.filters import Filter
from aiogram.types import Message

from bot.config import Config


class Scheduler(Filter):
    """
    Filter for checking if the user is an admin in a valid chat.
    """

    async def __call__(self, message: Message, config: Config) -> bool:
        """
        Check if the user is an admin in a valid chat.

        :param message: The message from Telegram.
        :param config: The configuration object from the loaded configuration.
        :return: True if the conditions for being an admin are met, False otherwise.
        """
        is_admin: bool = message.reply_to_message.from_user.id in config.tg_bot.admins
        is_admin_chat: bool = message.reply_to_message.chat.id in config.tg_bot.all_groups
        is_topic: bool = message.reply_to_message.message_thread_id is None

        return is_admin and is_admin_chat and is_topic
