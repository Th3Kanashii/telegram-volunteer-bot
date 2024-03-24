from __future__ import annotations

from typing import Optional, cast

from sqlalchemy import Select, Update, select, update

from ..models import Topic
from .base import BaseRepo


class TopicRepo(BaseRepo):
    """
    Repository for handling topic-related database operations.
    """

    async def get(self, user_id: int) -> Topic | None:
        """
        Retrieve a topic from the database.

        :param user_id: The ID of the user to retrieve the topic for.
        :return: The topic associated with the provided user ID.
        """
        return cast(
            Optional[Topic],
            await self._session.scalar(select(Topic).where(Topic.id == user_id)),
        )

    async def add(self, user_id: int, category: str, topic_id: int) -> None:
        """
        Add topic id in database.

        :param user_id: The ID of the user to add the topic to.
        :param category: The category to add the topic to.
        :param topic_id: The ID of the topic to add.
        """
        # Ensure valid attribute name before modification
        category_attribute = category + "_topic"
        if not hasattr(Topic, category_attribute):
            raise ValueError(f"Invalid attribute name: {category_attribute}")

        # Use parameterized query to set the attribute value
        statement: Update = (
            update(Topic).where(Topic.id == user_id).values({category_attribute: topic_id})
        )
        await self._session.execute(statement, params={"topic_id": topic_id})
        await self._session.commit()

    async def get_user_id(self, topic_id: int, category: str) -> Optional[int]:
        """
        Retrieve a user ID based on a specific topic ID and category.

        :param topic_id: The ID of the topic to search for.
        :param category: The category to search within.
        :return: The user ID associated with the provided topic and category.
        """
        # Validate category to prevent potential errors
        if not hasattr(Topic, f"{category}_topic"):
            raise ValueError(f"Invalid category: {category}")

        query: Select[tuple[int]] = select(Topic.id).where(
            getattr(Topic, f"{category}_topic") == topic_id
        )
        return cast(
            Optional[int], await self._session.scalar(query, params={"topic_id": topic_id})
        )
