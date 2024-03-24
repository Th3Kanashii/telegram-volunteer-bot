from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from aiogram.types import user
from aiogram_i18n.managers import BaseManager

if TYPE_CHECKING:
    from bot.services.database import RequestsRepo, User


class UserManager(BaseManager):
    """
    Middleware for installing and obtaining localization
    """

    async def get_locale(
        self, event_from_user: Optional[user.User] = None, user: Optional[User] = None
    ) -> str:
        if user:
            return user.locale
        if event_from_user:
            return event_from_user.language_code or cast(str, self.default_locale)
        return cast(str, self.default_locale)

    async def set_locale(self, locale: str, user: User, repo: RequestsRepo) -> None:
        user.locale = locale
        await repo.commit(user)
