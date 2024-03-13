from typing import Final

from aiogram import Bot, F, Router
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from bot.filters import JoinGroup
from bot.middlewares import AlbumMiddleware, ThrottlingMiddleware, TopicMiddleware

from . import from_user, help, language, new_member, start, subscription


async def set_user_commands(bot: Bot) -> None:
    """
    Set custom user interface commands.

    :param bot: The bot object used to interact with the Telegram API.
    """
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Main menu 📌"),
            BotCommand(command="help", description="Help 🤝"),
            BotCommand(command="language", description="Choose a language 🌐"),
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )


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


def get_user_router() -> Router:
    """
    Get a user router with filters and specific middlewares.

    :return: A user router with included filters and middlewares.
    """
    _setup_filters()
    _setup_middlewares()

    user_router: Final[Router] = Router(name=__name__)
    user_router.message.filter(F.chat.type == "private")
    user_router.include_routers(
        start.router,
        language.router,
        help.router,
        new_member.router,
        subscription.router,
        from_user.router,
    )
    return user_router


__all__ = [
    "get_user_router",
    "set_user_commands",
]
