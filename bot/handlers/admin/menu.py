from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Final

import aiofiles
from aiocsv import AsyncWriter
from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import TelegramMethod
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram_i18n import I18nContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.filters import Admin, Posting, Scheduler, SuperAdmin
from bot.keyboards import builder_inline

if TYPE_CHECKING:
    from bot.services.database import RequestsRepo

menu_router: Final[Router] = Router(name=__name__)


@menu_router.message(Command("help"), Admin())
async def help_command(message: Message, i18n: I18nContext) -> TelegramMethod[Any]:
    """
    Handler to /help commands.
    Responds with a help message providing information about available commands.

    :param message: The message from Telegram.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    return message.answer(text=i18n.get("help-admin", name=message.from_user.first_name))


@menu_router.message(Command("language"), Admin())
async def language_command(message: Message, i18n: I18nContext) -> TelegramMethod[Any]:
    """
    Handler to command /language.
    Send a message to choose a language.

    :param message: The message from Telegram.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    return message.answer(
        text=i18n.get("choose-a-language"),
        reply_markup=builder_inline(width=3, language_en="🇬🇧", language_uk="🇺🇦", language_ja="🇯🇵"),
    )


@menu_router.message(Command("cancel"), Admin())
async def cancel_command(message: Message, bot: Bot, state: FSMContext) -> bool | None:
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


@menu_router.message(Command("db"))
async def db_command(
    message: Message, repo: RequestsRepo, i18n: I18nContext
) -> TelegramMethod[Any]:
    """
    Handler to command /db.
    Send a CSV file with all users and their subscriptions.

    :param message: The message from Telegram.
    :param repo: The repository for database requests.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    users = await repo.users.get_data()
    headers: list[str] = [
        "Id",
        "Name",
        "Language",
        "Youth Policy",
        "Psychologist Support",
        "Civic Education",
        "Legal Support",
    ]
    subscription_counts: dict[str, int] = {
        "youth_policy": 0,
        "psychologist_support": 0,
        "civic_education": 0,
        "legal_support": 0,
        "subscription_count": 0,
    }

    async with aiofiles.open("users.csv", "w", newline="") as csvfile:
        writer = AsyncWriter(csvfile)
        await writer.writerow(headers)
        for user in users:
            for index, value in enumerate(user[3:]):
                if value:
                    subscription_counts["subscription_count"] += 1
                    subscription_counts[headers[index + 3].lower().replace(" ", "_")] += 1
            await writer.writerow(user)

    file: FSInputFile = FSInputFile("users.csv")

    subscription_percentages: dict[str, float] = {}
    for subscription_type, count in subscription_counts.items():
        if subscription_type != "subscription_count":
            percentage = (count / subscription_counts["subscription_count"]) * 100
            subscription_percentages[f"{subscription_type}_percentages"] = percentage

    caption = i18n.get(
        "get-db", users=len(users), **subscription_counts, **subscription_percentages
    )
    return message.answer_document(document=file, caption=caption)


@menu_router.message(Command("all", prefix="!"), SuperAdmin())
async def all_command(
    message: Message, bot: Bot, repo: RequestsRepo, i18n: I18nContext
) -> TelegramMethod[Any]:
    """
    Handler to command /all
    Send text messages to all users

    :param message: The message from Telegram.
    :param bot: The bot object used to interact with the Telegram API.
    :param repo: The repository for database requests.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    if not message.text or len(message.text) <= 4:
        return message.answer(text=i18n.get("something-went-wrong"))

    users = await repo.users.get_data()

    for user in users:
        try:
            await bot.send_message(chat_id=user[0], text=f"{message.text[4:]}")
            await asyncio.sleep(0.1)
        except TelegramBadRequest:
            continue

    return message.answer(text=i18n.get("all"))


@menu_router.message(Command("remove", prefix="!"), Scheduler(), F.reply_to_message)
async def remove_command(message: Message, bot: Bot, scheduler: AsyncIOScheduler) -> bool:
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


@menu_router.callback_query(F.data.startswith("language"))
async def process_set_the_language(
    callback: CallbackQuery, i18n: I18nContext
) -> TelegramMethod[Any]:
    """
    Handler admin callback for change language.
    Set the language for the admin.

    :param callback: The callback query from the admin.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    await i18n.set_locale(callback.data.split("_")[1])
    return callback.message.edit_text(text=i18n.get("admin-language"))
