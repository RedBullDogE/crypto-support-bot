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

from env import Env
from fiat_currencies_handling import fiat_handling
from messages import msg

API_TOKEN = os.getenv("API_TOKEN")

env = Env(init=True)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def cmd_start(message):
    """
    Message handler for /start command. Initialize bot menu.
    """

    main_menu_buttons = {}
    for field in fields(msg.main_menu):
        main_menu_buttons[field.name] = KeyboardButton(field.default)

    menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*main_menu_buttons.values())

    await message.reply(msg.common_messages.main_menu, reply_markup=menu)
    env.current_menu[message.chat.id] = "main_menu"


@dp.message_handler(content_types=['text'])
async def cmds_handler(message):
    """
    all message handler
    """

    if message.text == msg.main_menu.fiat_btn:
        await fiat_handling(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
