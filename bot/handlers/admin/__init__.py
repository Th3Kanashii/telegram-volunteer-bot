from aiogram import Router

from bot.filters import Admin, Scheduler, SuperAdmin
from bot.middlewares import AdminMiddleware, AlbumMiddleware

from . import from_forum, get_db, help, language, posting, remove_scheduler, send_all


def _setup_filters() -> None:
    """
    Setup filters for admin.
    """
    get_db.router.message.filter(Admin())
    help.router.message.filter(Admin())
    language.router.message.filter(Admin())
    posting.router.message.filter(Admin())
    remove_scheduler.router.message.filter(Scheduler())
    send_all.router.message.filter(SuperAdmin())
    from_forum.router.message.filter(Admin(command=False))


def _setup_middlewares() -> None:
    """
    Setup middlewares for admin.
    """
    from_forum.router.message.middleware(AlbumMiddleware())
    from_forum.router.message.middleware(AdminMiddleware())


def get_admin_routers() -> list[Router]:
    """
    Get a list of routers with admin filters and specific middlewares.

    :return: A list of routers with admin filters and middleware applied.
    """
    _setup_filters()
    _setup_middlewares()

    routers_list: list[Router] = [
        send_all.router,
        get_db.router,
        help.router,
        language.router,
        posting.router,
        remove_scheduler.router,
        from_forum.router,
    ]

    return routers_list


__all__ = [
    "get_admin_routers",
]
