from dataclasses import dataclass

from emoji import emojize


@dataclass(frozen=True)
class Messages:
    """
    Dataclass with bot messages
    """

    menu: str = "Hi! How can we help you?"

    help_btn: str = emojize("Help :green_book:")
    support_btn: str = emojize("Support :information:")
    about_btn: str = emojize("About Us :smiling_face_with_hearts:")
    fiat_btn: str = emojize("Fiat Exchanges :heavy_dollar_sign:")
    crypto_btn: str = emojize("Crypto Exchanges :currency_exchange:")


msg = Messages()
