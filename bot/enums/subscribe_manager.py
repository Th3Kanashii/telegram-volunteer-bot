from __future__ import annotations

from enum import Enum

from aiogram_i18n import LazyProxy


class SubscribeManager(Enum):
    """
    Manages subscription categories and provides utility methods for handling subscriptions.
    """

    __subscribe = [
        "youth-policy-not-sub",
        "psychologist-support-not-sub",
        "civic-education-not-sub",
        "legal-support-not-sub",
    ]
    __subscribed = [
        "youth-policy-sub",
        "psychologist-support-sub",
        "civic-education-sub",
        "legal-support-sub",
    ]
    __subscribe_values = {
        "youth-policy-not-sub": "youth-policy",
        "psychologist-support-not-sub": "psychologist-support",
        "civic-education-not-sub": "civic-education",
        "legal-support-not-sub": "legal-support",
    }

    @classmethod
    def get_subscribe_value(cls, category: str) -> str | None:
        """
        Gets the human-readable value category for a given subscription category.

        :param category: The subscription category.
        :return: The human-readable text category or None if not found.
        """
        for key, value in cls.__subscribe_values.items():
            if LazyProxy(key) == category or LazyProxy(key.replace("-not", "")) == category:
                return value
        return None

    @classmethod
    def get_subscribe(cls) -> list[LazyProxy]:
        """
        Gets a list of LazyProxy instances representing subscription categories to subscribe to.

        :return: List of LazyProxy instances representing subscription categories.
        """
        return [LazyProxy(category) for category in cls.__subscribe]

    @classmethod
    def get_subscribed(cls) -> list[LazyProxy]:
        """
        Gets a list of LazyProxy instances representing currently subscribed categories.

        :return: List of LazyProxy instances representing subscribed categories.
        """
        return [LazyProxy(category) for category in cls.__subscribed]

    @classmethod
    def invert_subscribe(cls) -> dict[str, LazyProxy]:
        """
        Inverts keys and replaces hyphens with underscores, creating LazyProxy objects for values.

        :return: A new dictionary with inverted key-value pairs.
        """
        return {v.replace("-", "_"): LazyProxy(k) for k, v in cls.__subscribe_values.items()}
