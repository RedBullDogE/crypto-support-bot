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
        return
    client = await AsyncClient().create()

    number_of_coins = int(re.findall(r'^\d+', message.text)[0]) if calculating else 1
    current_currency = re.findall(r'^\d+ *(.*)', message.text)[0] if calculating else message.text
    currency_exchange = ""
    if "->" not in current_currency:
        for currency in ["BUSD", "UAH", "BTC", "ETH", "USDT"]:
            if currency != current_currency:
                try:
                    res = await client.get_symbol_ticker(symbol=f"{current_currency}{currency}")
                    currency = "USD" if currency == "BUSD" else currency
                    currency_exchange += \
                        f"{number_of_coins} {current_currency}=" \
                        f"{'{:.10f}'.format(float(res['price']) * number_of_coins).rstrip('0').rstrip('.')} " \
                        f"{currency}\n"
                except BinanceAPIException:
                    # Binance does not always support information for the current currency
                    try:
                        res = await client.get_symbol_ticker(symbol=f"{currency}{current_currency}")
                        currency_exchange += \
                            f"{number_of_coins} {current_currency}=" \
                            f"{'{:.10f}'.format(1/(float(res['price']) * number_of_coins)).rstrip('0').rstrip('.')} " \
                            f"{currency}\n"
                    except BinanceAPIException:
                        currency_exchange += f"{current_currency} to {currency} not supported\n"
    else:
        currency, exchange_to = current_currency.split("->")[0].upper(), current_currency.split("->")[1].upper()
        exchange_to = f"B{exchange_to}" if exchange_to == "USD" else exchange_to
        try:
            res = await client.get_symbol_ticker(symbol=f"{currency}{exchange_to}")
            exchange_to = "USD" if exchange_to == "BUSD" else exchange_to
            currency_exchange += f"{number_of_coins} {currency}=" \
                                 f"{'{:.10f}'.format(float(res['price']) * number_of_coins).rstrip('0').rstrip('.')} " \
                                 f"{exchange_to}\n"
        except BinanceAPIException:
            try:
                res = await client.get_symbol_ticker(symbol=f"{exchange_to}{currency}")
                currency_exchange += \
                    f"{number_of_coins} {currency}=" \
                    f"{'{:.10f}'.format(1 / (float(res['price']) * number_of_coins)).rstrip('0').rstrip('.')} " \
                    f"{exchange_to}\n"
            except BinanceAPIException:
                currency_exchange += f"{currency} to {exchange_to} not supported\n"

    await message.reply(f"{currency_exchange}")

    await client.close_connection()


async def get_fiat_currency_info(message, calculating=False):
    """
        Get info about current fiat currency
    """
    if not check_correct_cmd(message.text, calculating):
        await message.reply(msg.common_messages.invalid_currency)
        return
    client = await AsyncClient().create()

    number_of_coins = int(re.findall(r'^\d+', message.text)[0]) if calculating else 1
    current_currency = re.findall(r'^\d+ *(.*)', message.text)[0] if calculating else message.text
    current_currency = f"B{current_currency}" if current_currency == "USD" else current_currency
    currency_exchange = ""
    if "->" not in current_currency:
        for currency in ["BUSD", "UAH", "EUR", "BTC", "ETH"]:
            if currency != current_currency:
                try:
                    eth_to_current_currency = await client.get_symbol_ticker(symbol=f"ETH{current_currency}")
                    eth_to_convert_currency = await client.get_symbol_ticker(symbol=f"ETH{currency}") \
                        if currency != "ETH" else {"price": 1}
                    res = float(eth_to_convert_currency["price"])/float(eth_to_current_currency["price"])
                    currency_exchange += f"{number_of_coins} {current_currency.replace('BUSD', 'USD')}=" \
                                         f"{'{:.10f}'.format(res/number_of_coins).rstrip('0').rstrip('.')} " \
                                         f"{currency.replace('BUSD', 'USD')}\n"
                except BinanceAPIException:
                    # Binance does not always support information for the current currency
                    currency_exchange += f"{current_currency.replace('BUSD', 'USD')} to " \
                                         f"{currency.replace('BUSD', 'USD')} not supported\n"
    else:
        currency, exchange_to = current_currency.split("->")[0].upper(), current_currency.split("->")[1].upper()
        currency = f"B{currency}" if currency == "USD" else currency
        exchange_to = f"B{exchange_to}" if exchange_to == "USD" else exchange_to
        try:
            eth_to_current_currency = await client.get_symbol_ticker(symbol=f"ETH{currency}")
            eth_to_convert_currency = await client.get_symbol_ticker(symbol=f"ETH{exchange_to}") \
                if currency != "ETH" else {"price": 1}
            res = float(eth_to_convert_currency["price"]) / float(eth_to_current_currency["price"])
            currency = "USD" if currency == "BUSD" else currency
            exchange_to = "USD" if exchange_to == "BUSD" else exchange_to
            currency_exchange += \
                f"{number_of_coins} {currency}={'{:.10f}'.format(res / number_of_coins).rstrip('0').rstrip('.')} " \
                f"{currency}\n"
        except BinanceAPIException:
            currency_exchange += f"{currency} to {exchange_to} not supported\n"

    await message.reply(f"{currency_exchange}")

    await client.close_connection()
