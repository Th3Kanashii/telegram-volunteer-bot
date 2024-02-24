from aiogram import Router

from bot.filters import JoinGroup
from bot.middlewares import AlbumMiddleware, ThrottlingMiddleware, TopicMiddleware

from . import from_user, help, language, new_member, start, subscription


def _setup_filters() -> None:
    """
    Setup filters for user.
    """
    new_member.router.message.filter(JoinGroup())


def _setup_middlewares() -> None:
    """
    Setup middlewares for user.
    """
    start.router.message.middleware(ThrottlingMiddleware(limit=2))
    language.router.message.middleware(ThrottlingMiddleware(limit=2))
    help.router.message.middleware(ThrottlingMiddleware(limit=2))
    subscription.router.message.middleware(ThrottlingMiddleware(limit=2))
    from_user.router.message.middleware(AlbumMiddleware())
    from_user.router.message.middleware(ThrottlingMiddleware())
    from_user.router.message.middleware(TopicMiddleware())


def get_user_routers() -> list[Router]:
    """
    Get a list of routers with user filters and specific middlewares.

    :return: A list of routers with user filters and middleware applied.
    """
    _setup_filters()
    _setup_middlewares()

    routers_list: list[Router] = [
        start.router,
        language.router,
        help.router,
        new_member.router,
        subscription.router,
        from_user.router,
    ]

    return routers_list


__all__ = [
    "get_user_routers",
]
