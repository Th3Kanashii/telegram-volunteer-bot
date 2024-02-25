from typing import Final

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router: Final[Router] = Router(name=__name__)


@router.message(Command("remove", prefix="!"), F.reply_to_message)
async def process_command_remove(message: Message, bot: Bot, scheduler: AsyncIOScheduler) -> bool:
    """
    Handler the !remove command.
    Remove a scheduled message.

    :param message: The message from Telegram.
    :param bot: The bot object used to interact with the Telegram API.
    :param scheduler: The scheduler for the APScheduler library.
    :return: The result of the bot.unpin_chat_message method.
    """
    scheduler.remove_job(str(message.reply_to_message.message_id))
    return await bot.unpin_chat_message(chat_id=message.reply_to_message.chat.id)
