from dataclasses import fields
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from helpers.messages import msg


def get_main_menu():
    main_menu_buttons = {}
    for field in fields(msg.main_menu):
        main_menu_buttons[field.name] = KeyboardButton(field.default)

    return ReplyKeyboardMarkup(resize_keyboard=True).add(*main_menu_buttons.values())


def get_admin_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("/admin"))


def get_support_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("/cancel"))
