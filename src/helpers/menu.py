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


def get_fiat_menu():
    fiat_menu_buttons = {}
    for field in fields(msg.fiat_currencies):
        fiat_menu_buttons[field.name] = KeyboardButton(field.default)

    cancel_btn = KeyboardButton(msg.common_messages.cancel_btn)
    return (
        ReplyKeyboardMarkup(resize_keyboard=True)
        .add(*fiat_menu_buttons.values())
        .row(cancel_btn)
    )


def get_crypto_menu():
    crypto_menu_buttons = {}
    for field in fields(msg.crypto_currencies):
        crypto_menu_buttons[field.name] = KeyboardButton(field.default)

    cancel_btn = KeyboardButton(msg.common_messages.cancel_btn)
    return (
        ReplyKeyboardMarkup(resize_keyboard=True)
        .add(*crypto_menu_buttons.values())
        .row(cancel_btn)
    )


def get_calculation_menu():
    cancel_btn = KeyboardButton(msg.common_messages.cancel_btn)
    return ReplyKeyboardMarkup(resize_keyboard=True).add(cancel_btn)


def get_admin_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("/admin"))


def get_support_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("/cancel"))
