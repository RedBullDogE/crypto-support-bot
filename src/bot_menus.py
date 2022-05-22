from aiogram.dispatcher.filters.state import State, StatesGroup


class Menus(StatesGroup):
    main_menu = State()
    help_menu = State()
    support_menu = State()
    about_menu = State()
    fiat_menu = State()
    crypto_menu = State()
    calculating_crypto = State()
