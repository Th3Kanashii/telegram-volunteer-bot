from __future__ import annotations

from typing import Optional, cast

from aiogram.types import User as TgUser
from aiogram_i18n import LazyProxy
from sqlalchemy import Row, select
from sqlalchemy.engine.result import Result

from bot.enums import SubscribeManager

from ..models import Topic, User
from .base import BaseRepo


class UserRepo(BaseRepo):
    """
    Repository class for handling operations related to users in the database.
    """

    async def get(self, user_id: int) -> User | None:
        """
        Retrieves a user from the database by their ID.

        :param user_id: The Telegram user ID.
        :return: User object or None if the user is not found.
        """
        return cast(
            Optional[User],
            await self._session.scalar(select(User).where(User.id == user_id)),
        )

    async def add(self, tg_user: TgUser) -> User:
        """
        Adds a user to the database or updates an existing user.

        :param tg_user: Object represents a Telegram user or bot.
        :return: Object User.
        """
        user: User = User(id=tg_user.id, name=tg_user.first_name, locale=tg_user.language_code)
        topic: Topic = Topic(id=tg_user.id)
        self._session.add_all([user, topic])
        await self._session.commit()

        return user

    async def update_subscription(self, user: User, category: str) -> None:
        """
        Renews or cancels a user's subscription to a category.

        :param user: The database user object.
        :param category: The category that the user wants to update.
        """
        key = SubscribeManager.get_subscribe_value(category=category).replace("-", "_")
        setattr(user, key, True)
        user.active_category = key

        await self._session.commit()

    async def unsubscribe(self, user: User) -> None:
        """
        Cancel user subscription

        :param user: The database user object.
        """
        setattr(user, user.active_category, False)
        user.active_category = None

        await self._session.commit()

    async def main_menu(self, user: User) -> None:
        """
        Back main menu the user

        :param user: The database user object.
        """
        user.active_category = None
        await self._session.commit()

    async def get_subscriptions(self, user: User) -> list[str]:
        """
        Gets a list of user subscriptions.

        :param user: The database user object.
        :param i18n: The internationalization context for language localization.
        :return: List of user subscriptions.
        """
        categories: dict[str, LazyProxy] = SubscribeManager.invert_subscribe()
        subscriptions: list[str] = [
            categories[category] for category in categories if getattr(user, category)
        ]
        return subscriptions

    async def get_data(self) -> list[Row[tuple[User]]]:
        """
        Retrieve user data from the database based on the provided fields.

        :param fields: A tuple of fields to retrieve.
        :return: A list of tuples containing user data.
        """
        result: Result[tuple[User]] = await self._session.execute(
            select(
                User.id,
                User.name,
                User.locale,
                User.youth_policy,
                User.psychologist_support,
                User.civic_education,
                User.legal_support,
            )
        )
        return list(result.all())
