from dataclasses import dataclass

from emoji import emojize


@dataclass(frozen=True)
class MainMenu:
    """
        Data class with main menu messages
    """
    help_btn: str = emojize("Help :green_book:")
    support_btn: str = emojize("Support :information:")
    about_btn: str = emojize("About Us :smiling_face_with_hearts:")
    fiat_btn: str = emojize("Fiat Exchanges :heavy_dollar_sign:")
    crypto_btn: str = emojize("Crypto Exchanges :currency_exchange:")


@dataclass(frozen=True)
class FiatCurrencies:
    """
        Data class with fiat currencies
    """
    usd_button: str = "USD"
    eur_button: str = "EUR"
    uah_button: str = "UAH"


@dataclass(frozen=True)
class CommonMessages:
    """
        Data class with common messages
    """
    main_menu: str = "Hi! How can we help you?"
    fiat_menu: str = "select a currency from the list for which to show information. If you need another currency, " \
                     "enter its code (example: for the hryvnia, the code is UAH)"


class Messages:
    """
    Class with all messages
    """

    common_messages = CommonMessages()
    main_menu = MainMenu()
    fiat_currencies = FiatCurrencies()


msg = Messages()
