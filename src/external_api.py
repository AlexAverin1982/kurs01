import json
import os.path

import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://www.cbr-xml-daily.ru/daily_json.js"


def get_stocks_url(symbol: str | list[str]) -> str:
    """
    Возвращает урл для апи, включая в себя ключ и коды акций
    :param symbol: список акций или один код акции
    :return: урл апи, чтобы узнать цены на акции
    """
    api_key = os.getenv("MARKET_STACK_API_KEY")
    if isinstance(symbol, str):
        stocks_url = f"http://api.marketstack.com/v1/eod/latest?access_key={api_key}&symbols={symbol}"
    elif isinstance(symbol, list):
        symbols = ",".join(symbol)
        stocks_url = f"http://api.marketstack.com/v1/eod/latest?access_key={api_key}&symbols={symbols}"
    else:
        stocks_url = f"http://api.marketstack.com/v1/eod/latest?access_key={api_key}"
    return stocks_url


def get_currency_rate(from_currency: str, to_currency: str) -> float:
    """
    Конвертируем валюту
    :param from_currency:  из
    :param to_currency: в
    :return: сколько
    """
    global url
    response = requests.get(url)
    if response.ok:
        s = response.text
        data = json.loads(s)
        text = data.get("text")
        data = json.loads(text)

        data_from = data.get(from_currency)
        if to_currency == "RUB":
            return data_from.get("Value")
        else:
            data_to = data.get(to_currency)
            if data_to:
                return data_from.get("Value") / data_to.get("Value", 1.0)
            else:
                return 0.0
    else:
        return 0.0


def get_overall_stocks(symbols_list: list[str]) -> list[dict]:  # вот это пока работает...
    """Используя API, грузим текущие цены на акции"""
    # api_key = os.getenv("MARKET_STACK_API_KEY")
    response = requests.get(get_stocks_url(symbols_list))
    if response.ok:
        data = json.loads(response.text)
        text = data.get("text")
        if text:
            data = json.loads(text).get("data")
        else:
            data = data.get("data")
        return data
    else:
        return []


def get_overall_currencies() -> list[dict]:
    """Используя API, грузим текущие курсы валют"""
    global url
    response = requests.get(url)
    if response.ok:
        data = response.text
        text = json.loads(data)
        return text
    else:
        return []


def get_stock_price(symbol: str) -> float:
    """Используя API, грузим текущие цены на акции"""
    response = requests.get(get_stocks_url(symbol))
    if response.ok:
        data = json.loads(response.text)
        text = data.get("text")
        data = json.loads(text)
        return data.get("data", [{}])[0].get("close", 0.0)
    else:
        return 0.0
