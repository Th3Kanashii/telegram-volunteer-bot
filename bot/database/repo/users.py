from __future__ import annotations

from aiogram.types import User as TgUser
from aiogram_i18n import LazyProxy
from sqlalchemy import Select, select
from sqlalchemy.engine.result import Result

from bot.enums import SubscribeManager

from ..models import User
from .base import BaseRepo


class UserRepo(BaseRepo):
    """
    Repository class for handling operations related to users in the database.
    """

    async def get_user(self, user_id: int) -> User | None:
        """
        Retrieves a user from the database by their ID.

        :param user_id: The Telegram user ID.
        :return: User object or None if the user is not found.
        """
        return await self.session.get(User, user_id)

    async def add_user(self, tg_user: TgUser) -> User:
        """
        Adds a user to the database or updates an existing user.

        :param tg_user: Object represents a Telegram user or bot.
        :return: Object User.
        """
        user: User = User(id=tg_user.id, name=tg_user.first_name, locale=tg_user.language_code)
        self.session.add(user)
        await self.session.commit()

        return user

    async def update_user_subscription(self, user: User, category: str) -> None:
        """
        Renews or cancels a user's subscription to a category.

        :param user: The database user object.
        :param category: The category that the user wants to update.
        """
        key = SubscribeManager.get_subscribe_value(category=category).replace("-", "_")
        setattr(user, key, True)
        user.active_category = key

        await self.session.commit()

    async def unsubscribe_user(self, user: User) -> None:
        """
        Cancel user subscription

        :param user: The database user object.
        """
        setattr(user, user.active_category, False)
        user.active_category = None

        await self.session.commit()

    async def main_user_menu(self, user: User) -> None:
        """
        Back main menu the user

        :param user: The database user object.
        """
        user.active_category = None
        await self.session.commit()

    async def get_user_subscriptions(self, user: User) -> list[str]:
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

    async def add_topic_id(self, user: User, topic_id: int) -> None:
        """
        Add topic id in database.

        :param user: The database user object.
        :param topic_id: The ID of the topic related to the user.
        """
        setattr(user, f"{user.active_category}_topic", topic_id)
        await self.session.commit()

    async def get_user_id_by_topic(self, topic_id: int, category: str) -> int | None:
        """
        Retrieve a user ID based on a specific topic ID and category.

        :param topic_id: The ID of the topic to search for.
        :param category: The category to search within.
        :return: The user ID associated with the provided topic and category.
        """
        query: Select[tuple[int]] = select(User.id).where(
            getattr(User, f"{category}_topic") == topic_id
        )
        return await self.session.scalar(query)

    async def get_user_data(self, fields: tuple[str]) -> list[tuple]:
        """
        Retrieve user data from the database based on the provided fields.

        :param fields: A tuple of fields to retrieve.
        :return: A list of tuples containing user data.
        """
        users: Result[tuple[User]] = await self.session.execute(select(User))
        user_data: list[tuple] = [
            tuple(getattr(user, field) for field in fields) for user in users.scalars()
        ]

        return user_data
