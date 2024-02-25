from typing import Final

from aiogram import F, Router

from .admin import get_admin_routers
from .commands import set_admin_commands, set_user_commands
from .user import get_user_routers


def _admin_router() -> Router:
    """
    Get the admin router.

    :return: A Router object for admin interactions.
    """
    admin_router: Final[Router] = Router(name=__name__)
    admin_router.message.filter(F.chat.type != "private")
    admin_router.include_routers(*get_admin_routers())
    return admin_router


def _user_router() -> Router:
    """
    Get the user router.

    :return: A Router object for user interactions.
    """
    user_router: Final[Router] = Router(name=__name__)
    user_router.message.filter(F.chat.type == "private")
    user_router.include_routers(*get_user_routers())
    return user_router


def get_routers() -> list[Router]:
    """
    Get the routers for the bot.

    :return: A list of Router objects.
    """
    return [
        _admin_router(),
        _user_router(),
    ]


__all__ = [
    "get_routers",
    "set_admin_commands",
    "set_user_commands",
]
