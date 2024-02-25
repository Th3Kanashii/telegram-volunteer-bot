from typing import Any, Final

from aiogram import Bot, Router, html
from aiogram.methods import TelegramMethod
from aiogram.types import InputMedia, Message

router: Final[Router] = Router(name=__name__)


@router.message()
async def process_from_forum(
    message: Message, bot: Bot, user_id: int, category: str, album: list[InputMedia] = None
) -> list[Message] | Message | TelegramMethod[Any]:
    """
    Handler messages from admin and copy them to a user chat.

    :param message: The message from Telegram.
    :param bot: The bot object used to interact with the Telegram API.
    :param user_id: The Telegram user ID.
    :param category: The category from admin.
    :param album: The list of media for creating a media album (optional).
    :return: TelegramMethod[Any] or Message or list[Message].
    """
    if album:
        return await bot.send_media_group(chat_id=user_id, media=album)
    if message.text:
        return await bot.send_message(
            chat_id=user_id,
            text=f"{html.bold(html.italic(category))}: {message.text}",
        )
    return message.copy_to(
        chat_id=user_id,
        caption=f"{html.bold(html.italic(category))}: "
        f"{message.caption if message.caption is not None else ''}",
    )
