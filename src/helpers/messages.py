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
    calculating_btn: str = "Calculating"


@dataclass(frozen=True)
class CryptoCurrencies:
    """
    Data class with cryptocurrencies
    """

    btc_button: str = "BTC"
    eth_button: str = "ETH"
    usdt_button: str = "USDT"
    calculating_btn: str = "Calculating"


@dataclass(frozen=True)
class CommonMessages:
    """
    Data class with common messages
    """

    main_menu: str = "Hi! How can we help you?"
    about_msg: str = emojize(
        ":sparkles:We are the CryptoApp team!:sparkles:\n\n"
        "Our values are convenience, speed and respect for people!:folded_hands:\n\n"
        "The project was created by a team of anonymous enthusiasts to make our world"
        " more technologically advanced and convenient.:rocket:\n\n"
        "This bot is designed to help you with the conversion of cryptocurrencies,"
        " recognition of rates, as well as support in case of questions about our platform."
    )

    help_msg: str = emojize(
        "This bot allows you to do the following:\n\n"
        " - Find out cryptocurrency rates\n"
        " - Find out fiat exchange rates\n"
        " - Cryptocurrency conversion\n"
        " - Answer the question to our support\n\n"
        "All these actions you can do by using the menu panel :index_pointing_up:"
    )
    currencies_menu: str = (
        "Select a cryptocurrency from the list for which to show information. If you need "
        "another currency, enter its code (example: for the Bitcoin, the code is BTC). you "
        "can also find out the exchange rate of one currency to another using the command "
        "{currency1->currency2}"
    )
    calculating_currency: str = (
        "Enter the number of coins in currency1 and the currency in which to show the result "
        "in the format {numbers currency1-> currency2}"
    )
    support_welcome: str = "Now you can answer the question to our support team!"
    support_bye: str = "Chat with the support team is closed"

    # Errors & Warnings
    invalid_currency: str = "Invalid request. Try again"
    no_active_admins: str = (
        "Sorry, there are no active admins now :c Please, contact us later"
    )

    # common buttons
    cancel_btn: str = emojize("Return to Menu :left_arrow:")


@dataclass(frozen=True)
class AdminMessages:

    admin_welcome: str = (
        "Admin mode is turned on. You will receive messages from clients as they appear"
    )
    admin_bye: str = (
        "Admin mode is turned off. You will no longer receive messages from clients"
    )


class Messages:
    """
    Class with all messages
    """

    common_messages = CommonMessages()
    admin_messages = AdminMessages()
    main_menu = MainMenu()
    fiat_currencies = FiatCurrencies()
    crypto_currencies = CryptoCurrencies()


msg = Messages()
