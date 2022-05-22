from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from dataclasses import fields

from bot_menus import Menus
from messages import msg


async def fiat_handling(message):
    """
    fiat currencies handling
    """

    fiat_menu_buttons = {}
    for field in fields(msg.fiat_currencies):
        fiat_menu_buttons[field.name] = KeyboardButton(field.default)

    menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*fiat_menu_buttons.values())

    await message.reply(msg.common_messages.currencies_menu, reply_markup=menu)
    await Menus.fiat_menu.set()
