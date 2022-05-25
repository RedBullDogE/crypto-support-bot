from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    main_menu = State()

    # support
    support_menu = State()
    admin = State()

    # exchanges
    fiat_menu = State()
    crypto_menu = State()
    calculating_fiat_currency = State()
    calculating_crypto_currency = State()
