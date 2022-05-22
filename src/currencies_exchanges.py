import re

from binance.exceptions import BinanceAPIException
from binance.client import AsyncClient

from messages import msg


def check_correct_cmd(cmd, calculated):
    reg_exp = r'[0-9]+ *([A-Za-z]{2,20}->[A-Za-z]{2,20})' if calculated else \
        r'([A-Za-z]{2,20}-*>*[A-Za-z]{0,20})'
    if re.findall(reg_exp, cmd):
        return True
    return False


async def get_crypto_currency_info(message, calculating: bool = False):
    """
        Get info about current cryptocurrency
    """
    if not check_correct_cmd(message.text, calculating):
        await message.reply(msg.common_messages.invalid_currency)
    client = await AsyncClient().create()

    number_of_coins = int(re.findall(r'^\d+', message.text)[0]) if calculating else 1
    current_currency = re.findall(r'^\d+ *(.*)', message.text)[0] if calculating else message.text
    currency_exchange = ""
    if "->" not in current_currency:
        for currency in ["BUSD", "UAH", "BTC", "ETH", "USDT"]:
            if currency != current_currency:
                try:
                    res = await client.get_symbol_ticker(symbol=f"{current_currency}{currency}")
                    currency_exchange += f"{number_of_coins} {current_currency}=" \
                                         f"{float(res['price'])*number_of_coins:.2f} {currency}\n"
                except BinanceAPIException:
                    # Binance does not always support information for the current currency
                    currency_exchange += f"{current_currency} to {currency} not supported\n"
    else:
        currency, exchange_to = current_currency.split("->")[0].upper(), current_currency.split("->")[1].upper()
        try:
            res = await client.get_symbol_ticker(symbol=f"{currency}{exchange_to}")
            currency_exchange += f"{number_of_coins} {currency}={float(res['price'])*number_of_coins:.2f} {currency}\n"
        except BinanceAPIException:
            currency_exchange += f"{currency} to {exchange_to} not supported\n"

    await message.reply(f"{currency_exchange}")

    await client.close_connection()
