from typing import Final

from aiogram import F, Router

from .from_forum import from_forum_router
from .menu import menu_router
from .posting import posting_router


def get_admin_router() -> Router:
    """
    Get a admin router with filters and specific middlewares.

    :return: A admin router with included filters and middlewares.
    """
    admin_router: Final[Router] = Router(name=__name__)
    admin_router.message.filter(F.chat.type != "private")
    admin_router.include_routers(
        menu_router,
        posting_router,
        from_forum_router,
    )
    return admin_router


__all__ = [
    "get_admin_router",
]
