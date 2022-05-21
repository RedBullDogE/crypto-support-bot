import os

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
