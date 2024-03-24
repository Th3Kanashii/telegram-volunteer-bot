from aiogram import Router

from .admin import get_admin_router
from .user import get_user_router


def get_routers() -> tuple[Router, Router]:
    """
    Get the routers for the bot.

    :return: A list of Router objects.
    """
    return get_admin_router(), get_user_router()


__all__ = [
    "get_routers",
]
