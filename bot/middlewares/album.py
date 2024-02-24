from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import InputMedia, InputMediaPhoto, Message


class AlbumMiddleware(BaseMiddleware):
    """
    Middleware for handling media albums in a Telegram bot.
    """

    __latency: float = 0.1
    __album_data: dict = {}

    @staticmethod
    def get_album(album: list[Message]) -> list[InputMedia]:
        """
        Creates a list of media elements suitable for creating an album.

        :param album: A list of Message objects representing the album content.
        :return: List of InputMedia objects for constructing a media album.
        """
        media_group = []
        for message in album:
            if message.photo:
                file_id = message.photo[-1].file_id
                media_group.append(InputMediaPhoto(media=file_id, caption=message.caption))
            else:
                obj_dict = message.model_dump()
                file_id = obj_dict[message.content_type]["file_id"]
                media_group.append(InputMedia(media=file_id, caption=message.caption))

        return media_group

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        try:
            self.__album_data[event.media_group_id].append(event)
        except KeyError:
            self.__album_data[event.media_group_id] = [event]
            await asyncio.sleep(self.__latency)
            data["album"] = self.get_album(album=self.__album_data[event.media_group_id])
            del self.__album_data[event.media_group_id]
            return await handler(event, data)
