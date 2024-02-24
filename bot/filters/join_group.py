from aiogram.filters import Filter
from aiogram.types import Message

from bot.config import Config


class JoinGroup(Filter):
    """
    This filter checks if the message is from the living library group.
    """

    async def __call__(self, message: Message, config: Config) -> bool:
        """
        Check if the message is from the living library group.

        :param message: The message from Telegram.
        :param config: The configuration object from the loaded configuration.
        :return: True if the message is from the living library group, False otherwise.
        """
        return message.chat.id == config.tg_bot.living_library
