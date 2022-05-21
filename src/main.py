import os

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from messages import msg

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def cmd_start(message):
    """
    Message handler for /start command. Initialize bot menu.
    """

    help_btn = KeyboardButton(msg.help_btn)
    support_btn = KeyboardButton(msg.support_btn)
    about_btn = KeyboardButton(msg.about_btn)
    fiat_btn = KeyboardButton(msg.fiat_btn)
    crypto_btn = KeyboardButton(msg.crypto_btn)

    menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
        help_btn, support_btn, about_btn, fiat_btn, crypto_btn
    )

    await message.reply(msg.menu, reply_markup=menu)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
