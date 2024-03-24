from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Final

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.filters import Posting
from bot.misc import send_posting

if TYPE_CHECKING:
    from bot.config import Config
    from bot.services.database import RequestsRepo

posting_router: Final[Router] = Router(name=__name__)


@posting_router.message(Command("posting"))
async def posting_command(
    message: Message, i18n: I18nContext, state: FSMContext
) -> TelegramMethod[Any]:
    """
    Handler the /post command.
    Initiating the process of scheduling posts.

    :param message: The message from Telegram.
    :param i18n: The internationalization context for language localization.
    :param state: The FSMContext to manage the conversation state.
    :return: A Telegram method.
    """
    await state.set_state(Posting.time)
    return message.answer(text=i18n.get("input-time"))


@posting_router.message(Posting.time)
async def process_posting_time(
    message: Message, i18n: I18nContext, state: FSMContext
) -> TelegramMethod[Any]:
    """
    Handler the message from admin and schedule it for posting.

    :param message: The message from Telegram.
    :param i18n: The internationalization context for language localization.
    :param state: The FSMContext to manage the conversation state.
    :return: A Telegram method.
    """
    try:
        posting_time = datetime.strptime(message.text, "%d.%m/%H:%M")  # noqa  DTZ007
        current_time = datetime.now()  # noqa  DTZ005
        current_time_format = current_time.strftime("%d.%m/%H:%M")
        current_time = datetime.strptime(current_time_format, "%d.%m/%H:%M")  # noqa  DTZ007
    except ValueError:
        return message.answer(text=i18n.get("something-went-wrong"))

    if posting_time < current_time:
        return message.answer(text=i18n.get("something-went-wrong"))

    time_difference = posting_time - current_time

    await state.update_data(
        time=datetime.now() + timedelta(seconds=time_difference.total_seconds())  # noqa  DTZ005
    )
    await state.set_state(Posting.message)

    return message.answer(text=i18n.get("input-message"))


@posting_router.message(Posting.message)
async def process_posting_message(
    message: Message,
    bot: Bot,
    repo: RequestsRepo,
    state: FSMContext,
    config: Config,
    scheduler: AsyncIOScheduler,
) -> bool:
    """
    Handler the message from admin and schedule it for posting.

    :param message: The message from Telegram.
    :param bot: The bot object used to interact with the Telegram API.
    :param repo: The repository for database requests.
    :param state: The FSMContext to manage the conversation state.
    :param config: The configuration settings.
    :param scheduler: The scheduler for the APScheduler library.
    :return: The result of the bot.pin_chat_message method.
    """
    data = await state.get_data()
    await state.clear()

    users = await repo.users.get_data()

    scheduler.add_job(
        send_posting,
        trigger="date",
        run_date=data["time"],
        kwargs={"message": message, "bot": bot, "config": config, "users": users},
        id=str(message.message_id),
    )

    await bot.delete_messages(
        chat_id=message.chat.id, message_ids=[message.message_id - id for id in range(1, 4)]
    )
    return await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.message_id)
