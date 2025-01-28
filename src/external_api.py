import os.path

import requests
from dotenv import load_dotenv
import json

load_dotenv()


def get_currency_rate(from_currency: str, to_currency: str) -> float:
    api_key = os.getenv("API_KEY")
    url = f"https://exchange-rates.abstractapi.com/v1/live/?api_key={api_key}&base={from_currency}&target={to_currency}"
    response = requests.get(url)
    # "https://exchange-rates.abstractapi.com/v1/live/?api_key=1cb8cc523f0c4aa7a5bacbb96a4be599&base=USD&target=EUR")
    if response.ok:
        content = json.loads(response.text)
        rate = content.get("exchange_rates")
        if rate:
            return rate.get("RUB", 0.0)
        else:
            return 0.0
    else:
        return 0.0


def get_overall_stocks(symbols_list: list[str]) -> list[dict]:
    """ Используя API, грузим текущие цены на акции """
    api_key = os.getenv("MARKET_STACK_API_KEY")
    symbols = ','.join(symbols_list)
    url = f"http://api.marketstack.com/v1/eod/latest?access_key={api_key}&symbols={symbols}"
    response = requests.get(url)
    if response.ok:
        return json.loads(response.text)
    else:
        return []


def get_overall_currencies(codes_list: list[str]) -> list[dict]:
    """ Используя API, грузим текущие курсы валют"""
    api_key = os.getenv("EXCHANGERATES_API_KEY")
    symbols = ','.join(codes_list)
    # url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={api_key}&symbols={symbols}&base=RUB"
    # url = f"https://api.exchangeratesapi.io/v1/latest?access_key={api_key}&base=RUB&symbols=GBP,JPY,EUR"
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    if response.ok:
        return json.loads(response.text)
    else:
        return []


def get_stock_price(stock: str, to_currency: str, date_start: str, date_end: str) -> float:
    api_key = os.getenv("FMP_API_KEY")

    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}"

    response = requests.get(url)
    if response.ok:
        content = json.loads(response.text)
        rate = content.get("exchange_rates")
        if rate:
            return rate.get("RUB", 0.0)
        else:
            return 0.0
    else:
        return 0.0


if __name__ == '__main__':
    """
    headers = {"apikey": api_key}
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={convert_to}&from={convert_from}&amount={amount}"
    response = requests.get(url, headers=headers)

    if response.ok:
    from_currency = 'USD'
    to_currency = 'RUB'
    """
