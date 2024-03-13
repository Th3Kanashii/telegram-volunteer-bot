from aiogram import Router

from .admin import get_admin_router, set_admin_commands
from .user import get_user_router, set_user_commands


def get_routers() -> list[Router]:
    """
    Get the routers for the bot.

    :return: A list of Router objects.
    """
    return [get_admin_router(), get_user_router()]


__all__ = [
    "get_routers",
    "set_admin_commands",
    "set_user_commands",
]
