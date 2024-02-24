from typing import Any, Final

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router: Final[Router] = Router(name=__name__)


@router.message(Command("remove", prefix="!"))
async def process_command_remove(message: Message, bot: Bot, scheduler: AsyncIOScheduler) -> Any:
    """
    Handler the !remove command.

    :param message: The message from Telegram.
    :param bot: The bot object used to interact with the Telegram API.
    :param scheduler: The scheduler for the APScheduler library.
    :return: A Telegram method or None.
    """
    job_id = str(message.reply_to_message.message_id)
    scheduler.remove_job(job_id)
    return await bot.unpin_chat_message(chat_id=message.reply_to_message.chat.id)
