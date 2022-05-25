import os

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from helpers.exceptions import NoAdmins
from helpers.menu import (
    get_admin_menu,
    get_crypto_menu,
    get_fiat_menu,
    get_main_menu,
    get_support_menu,
)
from helpers.states import UserStates, AdminStates
from currencies_exchanges import (
    get_crypto_currency_info,
    get_fiat_currency_info,
)
from helpers.messages import msg
from storage import Storage

API_TOKEN = os.getenv("API_TOKEN")

db = Storage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(state=None)
async def sync_admin(message):
    if not db.is_admin(message.from_user.id) or not db.is_admin_active(
        message.from_user.id
    ):
        await cmd_start(message)
        return

    await AdminStates.admin.set()


@dp.message_handler(state="*", commands=["start"])
async def cmd_start(message):
    """
    Message handler for /start command. Initialize bot menu.
    """

    await message.reply(msg.common_messages.main_menu, reply_markup=get_main_menu())
    await UserStates.main_menu.set()


@dp.message_handler(state="*", commands=["admin"])
async def cmd_admin(message):

    if db.is_admin_active(message.from_user.id):
        db.admin_mode(message.from_user.id, False)
        await message.reply(msg.admin_messages.admin_bye, reply_markup=get_main_menu())
        await UserStates.main_menu.set()
        return

    db.admin_mode(message.from_user.id, True)
    await AdminStates.admin.set()
    await message.reply(msg.admin_messages.admin_welcome, reply_markup=get_admin_menu())


@dp.message_handler(state=AdminStates.admin)
async def admin_support_handler(message):
    if not message.reply_to_message:
        return

    message_id = message.reply_to_message.message_id
    admin_id = message.chat.id

    user_id = db.get_target_user(admin_id, message_id)

    await bot.send_message(user_id, message.text)


@dp.message_handler(state=UserStates.main_menu, text=msg.main_menu.support_btn)
async def cmd_support(message):
    try:
        db.add_user_support(message.from_user.id)
    except NoAdmins:
        await message.reply(msg.common_messages.no_active_admins)
        return

    await UserStates.support_menu.set()
    await message.reply(
        msg.common_messages.support_welcome, reply_markup=get_support_menu()
    )


@dp.message_handler(state="*", commands=["cancel"])
async def cancel_handler(message, state):

    current_state = await state.get_state()

    # exit if user is in main menu
    if current_state is None or current_state == UserStates.main_menu.state:
        return

    # remove support record from db
    if current_state == UserStates.support_menu.state:
        db.remove_user_support(message.from_user.id)
        db.remove_target_user(message.from_user.id)

    # return to the main menu
    await cmd_start(message)


@dp.message_handler(state=UserStates.support_menu, content_types=["text"])
async def support_handler(message):
    admin_id = db.get_user_admin(message.from_user.id)

    if not db.is_admin_active(admin_id):
        try:
            admin_id = db.add_user_support(message.from_user.id)
        except NoAdmins:
            await message.reply(msg.common_messages.no_active_admins)
            return

    forward = await bot.forward_message(admin_id, message.chat.id, message.message_id)
    db.add_target_user(admin_id, forward.message_id, message.from_user.id)


@dp.message_handler(state=UserStates.main_menu, text=msg.main_menu.fiat_btn)
async def fiat_handler(message):
    """
    fiat currencies handling
    """

    await message.reply(
        msg.common_messages.currencies_menu, reply_markup=get_fiat_menu()
    )
    await UserStates.fiat_menu.set()


@dp.message_handler(state=UserStates.main_menu, text=msg.main_menu.crypto_btn)
async def crypto_handler(message):
    """
    cryptocurrencies handling
    """

    await message.reply(
        msg.common_messages.currencies_menu, reply_markup=get_crypto_menu()
    )
    await UserStates.crypto_menu.set()


@dp.message_handler(state=UserStates.crypto_menu, content_types=["text"])
async def crypto_menu_cmds(message):
    """
    crypto menu commands
    """
    if message.text == "Calculating":
        await message.reply(msg.common_messages.calculating_currency)
        await UserStates.calculating_crypto_currency.set()
    else:
        await get_crypto_currency_info(message, calculating=False)


@dp.message_handler(
    state=UserStates.calculating_crypto_currency, content_types=["text"]
)
async def calculating_crypto_cmds(message):
    """
    calculating crypto menu commands
    """
    await get_crypto_currency_info(message, calculating=True)


@dp.message_handler(state=UserStates.fiat_menu, content_types=["text"])
async def fiat_menu_cmds(message):
    """
    fiat menu commands
    """

    if message.text == "Calculating":
        await message.reply(msg.common_messages.calculating_currency)
        await UserStates.calculating_fiat_currency.set()
    else:
        await get_fiat_currency_info(message, calculating=False)


@dp.message_handler(state=UserStates.calculating_fiat_currency, content_types=["text"])
async def calculating_fiat_menu_cmds(message):
    """
    calculating fiat menu commands
    """

    await get_fiat_currency_info(message, calculating=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
