from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.config import Config
from bot.handlers import set_admin_commands, set_user_commands


async def _polling_startup(bot: Bot, config: Config, scheduler: AsyncIOScheduler) -> None:
    """
    Perform startup actions for the Telegram bot when using polling.

    :param bot: The instance of the Telegram bot.
    :param config: A configuration object containing necessary settings.
    """
    scheduler.start()
    await set_user_commands(bot=bot)
    await set_admin_commands(bot=bot, config=config)
    await bot.delete_webhook(drop_pending_updates=True)


async def run_polling(dp: Dispatcher, bot: Bot) -> None:
    """
    Run the Telegram bot with long polling.

    :param dp: The Dispatcher instance for the Telegram bot.
    :param bot: The instance of the Telegram bot.
    """
    dp.startup.register(_polling_startup)
    return await dp.start_polling(
        bot, allowed_updates=["message", "callback_query", "chat_member"]
    )
