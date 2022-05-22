import os

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from dataclasses import fields

from bot_menus import Menus
from crypto_currencies_handling import crypto_handling
from currencies_exchanges import get_crypto_currency_info
from fiat_currencies_handling import fiat_handling
from messages import msg

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(state='*', commands=["start"])
async def cmd_start(message):
    """
    Message handler for /start command. Initialize bot menu.
    """

    main_menu_buttons = {}
    for field in fields(msg.main_menu):
        main_menu_buttons[field.name] = KeyboardButton(field.default)

    menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*main_menu_buttons.values())

    await message.reply(msg.common_messages.main_menu, reply_markup=menu)
    await Menus.main_menu.set()


@dp.message_handler(state=Menus.main_menu, content_types=['text'])
async def cmds_handler(message):
    """
    all message handler
    """

    if message.text == msg.main_menu.fiat_btn:
        await fiat_handling(message)
    if message.text == msg.main_menu.crypto_btn:
        await crypto_handling(message)


@dp.message_handler(state=Menus.crypto_menu, content_types=['text'])
async def crypto_menu_cmds(message):
    """
        crypto menu commands
    """
    if message.text == "Calculating":
        await message.reply(msg.common_messages.calculating_crypto)
        await Menus.calculating_crypto.set()
    else:
        await get_crypto_currency_info(message, calculating=False)


@dp.message_handler(state=Menus.calculating_crypto, content_types=['text'])
async def crypto_menu_cmds(message):
    """
        calculating crypto menu commands
    """
    await get_crypto_currency_info(message, calculating=True)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
