from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeChat,
)

from bot.config import Config


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
