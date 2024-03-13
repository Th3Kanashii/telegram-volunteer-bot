import csv
from typing import Any, Final

import aiofiles
from aiogram import Router
from aiogram.filters import Command
from aiogram.methods import TelegramMethod
from aiogram.types import FSInputFile, Message
from aiogram_i18n import I18nContext

from bot.database import RequestsRepo

router: Final[Router] = Router(name=__name__)


@router.message(Command("db"))
async def process_command_get_db(
    message: Message, repo: RequestsRepo, i18n: I18nContext
) -> TelegramMethod[Any]:
    """
    Handler to /db commands.
    Generates a database report in the form of an Excel file and sends it.

    :param message: The message from Telegram.
    :param repo: The repository for database requests.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    headers: list[str] = [
        "ID",
        "Name",
        "Language",
        "Youth policy",
        "Psychologist support",
        "Civic education",
        "Legal support",
    ]
    fields: tuple[str, ...] = (
        "id",
        "name",
        "locale",
        "youth_policy",
        "psychologist_support",
        "civic_education",
        "legal_support",
    )

    data: list[tuple] = await repo.users.get_data(fields=fields)

    users = 0
    category_counts = [0, 0, 0, 0]

    async with aiofiles.open(file="users.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        await writer.writerow(headers)

        for row_data in data:
            users += 1
            if len(row_data) >= 8:
                for i in range(4, 8):
                    category_counts[i - 4] += 1 if row_data[i] else 0
            await writer.writerow(row_data)

    subscription_count = sum(category_counts)
    category_percentages: list[float | int] = [
        round((count / subscription_count) * 100, 1) if subscription_count > 0 else 0
        for count in category_counts
    ]
    file_data: FSInputFile = FSInputFile(path="users.csv", filename="users.csv")
    caption = i18n.get(
        "get-db",
        users=users,
        subscription_count=subscription_count,
        youth_policy=category_counts[0],
        youth_policy_percentages=category_percentages[0],
        psychologist_support=category_counts[1],
        psychologist_support_percentages=category_percentages[1],
        civic_education=category_counts[2],
        civic_education_percentages=category_percentages[2],
        legal_support=category_counts[3],
        legal_support_percentages=category_percentages[3],
    )

    return message.answer_document(document=file_data, caption=caption)
