from typing import Final

from aiogram import Bot, F, Router
from aiogram.types import BotCommand, BotCommandScopeChat

from bot.config import Config
from bot.filters import Admin, Scheduler, SuperAdmin
from bot.middlewares import AdminMiddleware, AlbumMiddleware

from . import from_forum, get_db, help, language, posting, remove_scheduler, send_all


async def set_admin_commands(bot: Bot, config: Config) -> None:
    """
    Set custom admin interface commands for each group chat based
    on the provided configuration.

    :param bot: The bot object used to interact with the Telegram API.
    :param config: The configuration object containing information about all group chats.
    """
    for chat_id in config.tg_bot.all_groups:
        await bot.set_my_commands(
            commands=[
                BotCommand(command="help", description="Help 🤝"),
                BotCommand(command="db", description="Database 🗃️"),
                BotCommand(command="posting", description="Posting 📝"),
                BotCommand(command="language", description="Choose a language 🌐"),
            ],
            scope=BotCommandScopeChat(chat_id=chat_id),
        )


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


def get_admin_router() -> Router:
    """
    Get a admin router with filters and specific middlewares.

    :return: A admin router with included filters and middlewares.
    """
    _setup_filters()
    _setup_middlewares()

    admin_router: Final[Router] = Router(name=__name__)
    admin_router.message.filter(F.chat.type != "private")
    admin_router.include_routers(
        send_all.router,
        get_db.router,
        help.router,
        language.router,
        posting.router,
        remove_scheduler.router,
        from_forum.router,
    )
    return admin_router


__all__ = [
    "get_admin_router",
    "set_admin_commands",
]
