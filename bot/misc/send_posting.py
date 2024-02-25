import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from bot.config import Config


async def send_posting(message: Message, bot: Bot, config: Config, users: list[tuple]) -> bool:
    """
    Send posting to all users in category

    :param message: message from user
    :param bot: The bot object used to interact with the Telegram API.
    :param config: The configuration object.
    :param users: list of users.
    :return: The Telegram method.
    """
    categories: dict[int, int] = {
        config.tg_bot.youth_policy: 1,
        config.tg_bot.psychologist_support: 2,
        config.tg_bot.civic_education: 3,
        config.tg_bot.legal_support: 4,
    }
    category = categories.get(message.chat.id)
    for user in users:
        try:
            if user[category]:
                await message.copy_to(chat_id=user[0])
                await asyncio.sleep(0.1)
        except TelegramBadRequest:
            continue

    return await bot.unpin_chat_message(chat_id=message.chat.id, message_id=message.message_id)
