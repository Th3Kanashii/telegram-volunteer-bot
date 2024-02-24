from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram_i18n import I18nContext
from aiogram_i18n.types import KeyboardButton


def builder_reply(
    *texts: str,
    is_persistent: bool | None = None,
    resize_keyboard: bool | None = True,
    one_time_keyboard: bool | None = None,
    input_field_placeholder: str | None = None,
    selective: bool | None = None,
    width: int = 2,
) -> ReplyKeyboardMarkup:
    """
    Constructs a ReplyKeyboardMarkup using the provided text buttons.

    :param texts: Variable number of strings representing the text for each button.
    :param is_persistent: If True, the keyboard is persistent. Default is None.
    :param resize_keyboard: If True, the keyboard is resized. Default is True.
    :param one_time_keyboard: If True, the keyboard is displayed only once. Default is None.
    :param input_field_placeholder: Placeholder text for the input field. Default is None.
    :param selective: (Optional) If True, the keyboard is selective. Default is None.
    :param width: (Optional) Number of buttons in each row. Default is 2.

    :return: ReplyKeyboardMarkup object representing the constructed keyboard.
    """
    builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    builder.row(*[KeyboardButton(text=text) for text in texts], width=width)
    return builder.as_markup(
        is_persistent=is_persistent,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        input_field_placeholder=input_field_placeholder,
        selective=selective,
    )


def start(i18n: I18nContext, subscriptions: list[str]) -> ReplyKeyboardMarkup:
    """
    Generates a reply keyboard for starting a chat session.

    :param i18n: The internationalization context for language localization.
    :param subscriptions: A list of subscription categories.
    :return: A reply keyboard markup with options for subscription category.
    """
    categories: list[str] = i18n.get("categories").split(",")
    keyboard: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    for category in categories:
        category = category.strip()
        if category in subscriptions:
            keyboard.row(KeyboardButton(text=category.replace(category.split()[-1], "✅")))
        else:
            keyboard.row(KeyboardButton(text=category))

    return keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder=i18n.get("placeholder-subscribe"),
    )
