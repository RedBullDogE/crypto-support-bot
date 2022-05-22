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
    crypto_currencies_menu: str = "Select a cryptocurrency from the list for which to show information. If you need " \
                                  "another currency, enter its code (example: for the Bitcoin, the code is BTC). you " \
                                  "can also find out the exchange rate of one currency to another using the command " \
                                  "{currency1->currency2}"
    calculating_crypto: str = "Enter the number of coins in currency1 and the currency in which to show the result " \
                              "in the format {numbers currency1-> currency2}"
    invalid_currency: str = "Invalid request. Try again"


class Messages:
    """
    Class with all messages
    """

    common_messages = CommonMessages()
    main_menu = MainMenu()
    fiat_currencies = FiatCurrencies()
    crypto_currencies = CryptoCurrencies()


msg = Messages()
