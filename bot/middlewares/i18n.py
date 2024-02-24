from __future__ import annotations

from typing import cast

from aiogram.types import user
from aiogram_i18n.managers import BaseManager

from bot.database import RequestsRepo, User


class UserManager(BaseManager):
    """
    Middleware for installing and obtaining localization
    """

    async def get_locale(self, event_from_user: user.User, user: User) -> str:
        if user:
            return user.locale
        if event_from_user:
            return event_from_user.language_code or cast(str, self.default_locale)
        return cast(str, self.default_locale)

    async def set_locale(self, locale: str, user: User, repo: RequestsRepo) -> None:
        user.locale = locale
        await repo.commit(user)
