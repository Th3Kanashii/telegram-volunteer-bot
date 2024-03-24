from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Bot, F, Router
from aiogram.methods import TelegramMethod
from aiogram.types import ChatMemberMember, Message, ReplyKeyboardMarkup
from aiogram_i18n import I18nContext, LazyProxy

from bot.enums import SubscribeManager
from bot.keyboards import builder_reply, living_library, start

from ..ui_commands import set_user_commands

if TYPE_CHECKING:
    from bot.config import Config
    from bot.services.database import RequestsRepo, User

subscription_router: Final[Router] = Router(name=__name__)


@subscription_router.message(F.text.in_(SubscribeManager.get_subscribe()))
async def process_subscribe(
    message: Message, user: User, repo: RequestsRepo, i18n: I18nContext
) -> TelegramMethod[Any]:
    """
    Handler user subscription to specific categories.

    :param message: The message from Telegram.
    :param user: The database user object.
    :param repo: The repository for database requests.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    await repo.users.update_subscription(user=user, category=message.text)
    return message.answer(
        text=i18n.get(SubscribeManager.get_subscribe_value(category=message.text)),
        reply_markup=builder_reply(
            *[i18n.get("cancel-subscribe"), i18n.get("main-menu")],
            input_field_placeholder=i18n.get("placeholder-write-message"),
        ),
    )


@subscription_router.message(F.text.in_(SubscribeManager.get_subscribed()))
async def process_subscribed(
    message: Message, user: User, repo: RequestsRepo, i18n: I18nContext
) -> TelegramMethod[Any]:
    """
    Handler user subscribed.

    :param message: The message from Telegram.
    :param user: The database user object
    :param repo: The repository for database requests.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    keyboard: ReplyKeyboardMarkup = builder_reply(
        *[i18n.get("cancel-subscribe"), i18n.get("main-menu")],
        input_field_placeholder=i18n.get("placeholder-write-message"),
    )
    await repo.users.update_subscription(user=user, category=message.text)

    if message.text == i18n.get("civic-education-sub"):
        return message.answer(text=i18n.get("volunteer-not-active"), reply_markup=keyboard)
    return message.answer(text=i18n.get("subscribed"), reply_markup=keyboard)


@subscription_router.message(
    F.text == LazyProxy("living-library-btn"), flags={"throttling_key": "default"}
)
async def process_living_library(
    message: Message, bot: Bot, i18n: I18nContext, config: Config
) -> TelegramMethod[Any]:
    """
    Handler to provide a link to the live library chat.

    :param message: The message from Telegram.
    :param bot: The bot object used to interact with the Telegram API.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    member: ChatMemberMember = await bot.get_chat_member(
        chat_id=config.tg_bot.living_library_username, user_id=message.from_user.id
    )
    return message.answer(
        text=i18n.get("living-library"),
        reply_markup=living_library(member=member, i18n=i18n, config=config),
    )


@subscription_router.message(F.text == LazyProxy("cancel-subscribe"))
async def process_unsubscribe(
    message: Message, user: User, repo: RequestsRepo, i18n: I18nContext
) -> TelegramMethod[Any]:
    """
    Handler user cancellation of subscriptions.

    :param message: The message from Telegram.
    :param user: The database user object.
    :param repo: The repository for database requests.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    await repo.users.unsubscribe(user=user)
    subscriptions: list[str] = await repo.users.get_subscriptions(user=user)

    return message.answer(
        text=i18n.get("subscription-cancelled"),
        reply_markup=start(subscriptions=subscriptions, i18n=i18n),
    )


@subscription_router.message(F.text == LazyProxy("main-menu"))
async def process_main_menu(
    message: Message, user: User, repo: RequestsRepo, i18n: I18nContext
) -> TelegramMethod[Any]:
    """
    Handler a return to the main menu.

    :param message: The message from Telegram.
    :param user: The database user object.
    :param repo: The repository for database requests.
    :param i18n: The internationalization context for language localization.
    :return: A Telegram method.
    """
    subscriptions: list[str] = await repo.users.get_subscriptions(user=user)
    await repo.users.main_menu(user=user)

    return message.answer(
        text=i18n.get("back-menu"), reply_markup=start(subscriptions=subscriptions, i18n=i18n)
    )


@subscription_router.message(F.text.in_(["EN 🇬🇧", "UA 🇺🇦", "JA 🇯🇵"]))
async def process_set_the_language(
    message: Message, bot: Bot, user: User, i18n: I18nContext, repo: RequestsRepo
) -> TelegramMethod[Any]:
    """
    Handler for processing language selection in the Telegram bot.

    :param message: The message from Telegram.
    :param bot: The bot object used to interact with the Telegram API.
    :param user: The database user object.
    :param i18n: The internationalization context for language localization.
    :param repo: The repository for database requests.
    :return: A Telegram method.
    """
    subscriptions: list[str] = await repo.users.get_subscriptions(user=user)
    await i18n.set_locale(message.text.split()[0].lower() if message.text != "UA 🇺🇦" else "uk")
    await set_user_commands(bot=bot, i18n=i18n, chat_id=user.id)

    return message.answer(
        text=i18n.get("start", name=message.from_user.first_name),
        reply_markup=start(subscriptions=subscriptions, i18n=i18n),
    )
