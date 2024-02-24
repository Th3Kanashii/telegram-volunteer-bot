import asyncio

from aiogram import Bot, Dispatcher

from bot.config import Config, load_config
from bot.core import create_bot, create_dispatcher, run_polling
from bot.utils import setup_logging


async def main() -> None:
    setup_logging()
    config: Config = load_config(path=".env")
    dp: Dispatcher = create_dispatcher(config=config)
    bot: Bot = create_bot(config=config)
    return await run_polling(dp=dp, bot=bot)


if __name__ == "__main__":
    asyncio.run(main())
