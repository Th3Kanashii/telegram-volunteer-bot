from typing import Any, Final

from aiogram import Bot, F, Router
from aiogram.methods import TelegramMethod
from aiogram.types import ChatMemberMember, Message
from aiogram_i18n import I18nContext, LazyProxy

from bot.config import Config
from bot.database import RequestsRepo, User
from bot.enums import SubscribeManager
from bot.keyboards import builder_reply, living_library, start

router: Final[Router] = Router(name=__name__)


@router.message(F.text.in_(SubscribeManager.get_subscribe()))
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
    text = SubscribeManager.get_subscribe_value(category=message.text)
    await repo.users.update_subscription(user=user, category=message.text)
    return message.answer(
        text=i18n.get(text),
        reply_markup=builder_reply(
            *[i18n.get("cancel-subscribe"), i18n.get("main-menu")],
            input_field_placeholder=i18n.get("placeholder-write-message"),
        ),
    )


@router.message(F.text.in_(SubscribeManager.get_subscribed()))
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
    await repo.users.update_subscription(user=user, category=message.text)
    if message.text == i18n.get("civic-education-sub"):
        return message.answer(
            text=i18n.get("volunteer-not-active"),
            reply_markup=builder_reply(
                *[i18n.get("cancel-subscribe"), i18n.get("main-menu")],
                input_field_placeholder=i18n.get("placeholder-write-message"),
            ),
        )
    return message.answer(
        text=i18n.get("subscribed"),
        reply_markup=builder_reply(
            *[i18n.get("cancel-subscribe"), i18n.get("main-menu")],
            input_field_placeholder=i18n.get("placeholder-write-message"),
        ),
    )


@router.message(F.text == LazyProxy("living-library-btn"), flags={"throttling_key": "default"})
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


@router.message(F.text == LazyProxy("cancel-subscribe"))
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


@router.message(F.text == LazyProxy("main-menu"))
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
