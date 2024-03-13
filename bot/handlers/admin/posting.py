from datetime import datetime, timedelta
from typing import Any, Final

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import TelegramMethod
from aiogram.types import Message
from aiogram_i18n import I18nContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.config import Config
from bot.database import RequestsRepo
from bot.filters import Posting
from bot.misc import send_posting

router: Final[Router] = Router(name=__name__)


@router.message(Command("posting"))
async def process_command_posting(
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


@router.message(Command("cancel"))
async def process_command_cancel(message: Message, bot: Bot, state: FSMContext) -> bool | None:
    """
    Handler the /cancel command.
    Initiating the process of cancel state.

    :param message: The message from Telegram.
    :param state: The FSMContext to manage the conversation state.
    :return: None if the current conversation state is None.
             Otherwise, clears the state, deletes messages, and returns bot.delete_messages result.
    """
    current_state = await state.get_state()
    if current_state is None:
        return None

    await state.clear()
    messages_ids = 3 if current_state == Posting.time else 5

    return await bot.delete_messages(
        chat_id=message.chat.id,
        message_ids=[message.message_id - id for id in range(messages_ids)],
    )


@router.message(Posting.time)
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
        posting_time = datetime.strptime(message.text, "%d.%m/%H:%M")
        current_time = datetime.now()
        current_time_format = current_time.strftime("%d.%m/%H:%M")
        current_time = datetime.strptime(current_time_format, "%d.%m/%H:%M")
    except ValueError:
        return message.answer(text=i18n.get("something-went-wrong"))

    if posting_time < current_time:
        return message.answer(text=i18n.get("something-went-wrong"))

    time_difference = posting_time - current_time

    await state.update_data(
        time=datetime.now() + timedelta(seconds=time_difference.total_seconds())
    )
    await state.set_state(Posting.message)

    return message.answer(text=i18n.get("input-message"))


@router.message(Posting.message)
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

    fields: tuple[str, ...] = (
        "id",
        "youth_policy",
        "psychologist_support",
        "civic_education",
        "legal_support",
    )
    users: list[tuple] = await repo.users.get_data(fields=fields)

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
