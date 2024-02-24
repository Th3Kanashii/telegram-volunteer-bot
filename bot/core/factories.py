from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.config import Config
from bot.database import create_pool
from bot.handlers import get_routers
from bot.middlewares import (
    DatabaseMiddleware,
    SchedulerMiddleware,
    UserManager,
    UserMiddleware,
)


def _setup_outer_middlewares(dp: Dispatcher, config: Config) -> None:
    """
    Register global middlewares for the given dispatcher.

    :param dp: The dispatcher instance.
    :param config: The configuration object from the loaded configuration.

    The function registers the following global middlewares for message and
    callback_query handling:
    1. DatabaseMiddleware: Integrating database operations using SQLAlchemy.
    2. UserMiddleware: Object user database.
    3. I18nMiddleware: Internationalization middleware for handling translations.
    """
    session_pool = dp["session_pool"] = create_pool(dsn=config.db.construct_sqlalchemy_url())
    i18n_middleware = dp["i18n_middleware"] = I18nMiddleware(
        core=FluentRuntimeCore(path="locales/{locale}/LC_MESSAGES"), manager=UserManager()
    )
    scheduler = dp["scheduler"] = AsyncIOScheduler(timezone="Europe/Kyiv")

    dp.update.outer_middleware(DatabaseMiddleware(session_pool=session_pool))
    dp.update.outer_middleware(UserMiddleware())
    dp.update.outer_middleware(SchedulerMiddleware(scheduler=scheduler))
    i18n_middleware.setup(dispatcher=dp)


def create_dispatcher(config: Config) -> Dispatcher:
    """
    Creates and configures a Telegram bot dispatcher.

    :param config: A configuration object containing necessary settings.
    :return: An instance of the Dispatcher for the Telegram bot.
    """
    dp: Dispatcher = Dispatcher(name="main_dispatcher", storage=MemoryStorage(), config=config)
    dp.include_routers(*get_routers())
    _setup_outer_middlewares(dp=dp, config=config)
    return dp


def create_bot(config: Config) -> Bot:
    """
    Creates a Telegram bot instance.

    :param config: A configuration object containing necessary settings.
    :return: An instance of the Telegram bot.
    """
    session: AiohttpSession = AiohttpSession()
    return Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML, session=session)
