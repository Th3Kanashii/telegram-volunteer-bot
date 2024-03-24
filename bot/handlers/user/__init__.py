from typing import Final

from aiogram import F, Router

from .from_user import from_user_router
from .menu import menu_router
from .new_member import new_member_router
from .subscription import subscription_router


def get_user_router() -> Router:
    """
    Get a user router with filters and specific middlewares.

    :return: A user router with included filters and middlewares.
    """
    user_router: Final[Router] = Router(name=__name__)
    user_router.message.filter(F.chat.type == "private")
    user_router.include_routers(
        menu_router,
        new_member_router,
        subscription_router,
        from_user_router,
    )
    return user_router


__all__ = [
    "get_user_router",
]
