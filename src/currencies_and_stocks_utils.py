import datetime as dt
import os
import json
from datetime import datetime as datetime
from datetime import timedelta as tdelta
from time import strptime, strftime
from pandas import read_excel, DataFrame, to_datetime
from math import isnan

from src.external_api import get_currency_rate, get_stock_price, get_overall_stocks, get_overall_currencies

CURRENCIES_AVAILABLE = {'USD': 'Американский доллар',
                        'EUR': 'Евро',
                        'CAD': 'Канадский доллар',
                        'AUD': 'Австралийский доллар',
                        'CNY': 'Юань',
                        'DOP': 'Доминиканское песо',
                        'HKD': 'Гонконгский доллар',
                        'INR': 'Индийская рупия',
                        'IRR': 'Иранский риал',
                        'ILS': 'Новый израильский шекель',
                        'JPY': 'Иена',
                        }

user_currencies = {}

user_stocks = {}

stocks_cache = []

currencies_cache = []

""" 
        print('1. Загрузить валюты и акции из файла JSON')
        print('2. Ввести валюты вручную')
        print('3. Ввести акции вручную')
        print('4. Информация о валютах и акциях')
        print('5. Сохранить валюты и акции в файл JSON')

"""


def load_currencies_and_stocks_from_json(filename: str) -> dict:
    """ Функция принимает на вход путь до JSON-файла
    и возвращает список кодов валют и акций, интересующих пользователя """
    result = []
    if os.path.exists(filename) and os.path.isfile(filename):
        try:
            with open(filename, encoding="utf-8") as f:
                result = json.load(f)
            # utils_logger.info(f"файл {filename} с данными операций загружен успешно")
        except json.JSONDecodeError as ex:
            result = []
            # utils_logger.error(ex)
    else:
        # utils_logger.error(f"файл {filename} не найден")
        result = []
    return result


def get_currencies_rates(data: dict) -> list[dict]:
    """ Получаем список словарей с ценами валют, полученными по API """
    global currencies_cache

    result = []
    for currency_code in data.get('user_currencies', []):
        currency = {"currency": currency_code, "rate": round(currencies_cache[currency_code]['Value'], 2)}
        result.append(currency)
    return result


def get_stocks_prices(data: dict) -> list[dict]:
    """ Получаем список словарей с ценами акций, полученными по API """
    global stocks_cache
    if not stocks_cache:
        cache_stocks()
    result = []
    for stock_code in data.get('user_stocks', []):
        stock = {"stock": stock_code, "price": stocks_cache[stock_code]}
        result.append(stock)
    return result


def select_users_currencies() -> dict:
    """ Выбираем валюты, интересующие пользователя """
    global user_currencies
    print('Введите через запятую номера интересующих валют')
    print('Или *, чтобы выбрать все валюты')
    print('Любая другая строка - отмена выбора\n')

    i = 1
    for code, description in CURRENCIES_AVAILABLE.items():
        print(f"{i}. {code} --- {description}")
        i += 1

    user_input = input('Ваш выбор: ')
    if user_input == '*':
        user_currencies = {code: get_currency_rate(code, 'RUB') for code in CURRENCIES_AVAILABLE.keys()}
    elif user_input.find(',') > 0:
        indices = user_input.split(',')
        indices = [int(i) for i in indices]
        user_currencies = {code: get_currency_rate(code, 'RUB') for i, code in enumerate(CURRENCIES_AVAILABLE.keys()) if
                           i + 1 in indices}
    else:
        print('Выбран основной набор валют: USD, EUR, CNY')
        user_currencies = {code: get_currency_rate(code, 'RUB') for code in ['USD', 'EUR', 'CNY']}

    return user_currencies


def show_users_rates(items: dict, header: str = '') -> None:
    """ Выводим курсы валют """
    print('\n')
    if header:
        print(header)
    for code, rate in items.items():
        print(f"1 {code} == {round(rate, 2)} руб.")
    print('\n')


def select_users_stocks() -> dict:
    """ Выбираем акции, интересующие пользователя """
    global user_stocks
    print('Введите через запятую коды интересующих акций')
    print('Любая другая строка - отмена выбора\n')

    # i = 1
    # for code, description in CURRENCIES_AVAILABLE.items():
    #     print(f"{i}. {code} --- {description}")
    #     i += 1

    user_input = input('Ваш выбор: ')
    # if user_input == '*':
    #     user_stocks = {code: get_currency_rate(code, 'RUB') for code in CURRENCIES_AVAILABLE.keys()}
    if user_input.find(',') > 0:
        stocks = user_input.split(',')
        user_stocks = {code: get_stock_price(code, 'RUB') for code in stocks}
    # else:
    #     print('Выбран основной набор валют: USD, EUR, CNY')
    #     user_currencies = {code: get_currency_rate(code, 'RUB') for code in ['USD', 'EUR', 'CNY']}

    return user_stocks


def save_currencies_and_stocks_to_json(filename: str) -> None:
    """ Сохраняем акции и валюты, интересующие пользователя в файл предпочтений пользователя """
    global user_stocks, user_currencies
    data_to_write = {"user_currencies": user_currencies.keys(), "user_stocks": user_stocks.keys()}
    with open(filename, 'w') as f:
        json.dump(data_to_write, f)


def cache_stocks(file_cache_is_enough: bool = True) -> dict:
    """ Читаем кэш данных по акциям из файла и при необходиомости обновляем его через API """
    global stocks_cache
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    user_filename = os.path.join(par_dir, "user_settings.json")
    cache_filename = os.path.join(par_dir, "cache", "stocks_cache.json")
    currencies_and_stocks = load_currencies_and_stocks_from_json(user_filename)

    read_from_file = []
    symbols_to_read = []
    if os.path.exists(cache_filename):
        with open(cache_filename, encoding="utf-8") as f:
            read_from_file = json.load(f)
        symbols_read = set([stock_dict.get('symbol', '') for stock_dict in read_from_file])
        symbols_to_read = set(currencies_and_stocks["user_stocks"])
        symbols_to_read = symbols_to_read.difference(symbols_read)

    if len(symbols_to_read) or (not file_cache_is_enough) or (not read_from_file):
        if symbols_to_read:
            stocks_cache = get_overall_stocks(list(symbols_to_read))
        else:
            stocks_cache = get_overall_stocks(currencies_and_stocks["user_stocks"])
        data_to_write = []
        if stocks_cache:
            for stock in stocks_cache['data']:
                stock_dict = {"symbol": stock["symbol"],
                              "price": stock["close"]}
                data_to_write.append(stock_dict)
            read_from_file.extend(data_to_write)

        if read_from_file:
            with open(cache_filename, 'w') as f:
                json.dump(read_from_file, f, indent=4)

    stocks_cache = read_from_file
    convert_stocks_prices()
    stocks_cache = convert_to_dict(stocks_cache, 'symbol', 'price')
    return stocks_cache


def cache_currencies(file_cache_is_enough: bool = True) -> list[dict]:
    """ Читаем кэш данных по валютам из файла и при необходиомости обновляем его через API """
    global currencies_cache
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    user_filename = os.path.join(par_dir, "user_settings.json")
    cache_filename = os.path.join(par_dir, "cache", "currencies_cache.json")
    currencies_and_stocks = load_currencies_and_stocks_from_json(user_filename)

    read_from_file = {}
    codes_to_read = []
    if os.path.exists(cache_filename):
        with open(cache_filename, encoding="utf-8") as f:
            read_from_file = json.load(f)
        codes_read = set(read_from_file.keys())
        codes_to_read = set(currencies_and_stocks["user_currencies"])
        codes_to_read = codes_to_read.difference(codes_read)

    if len(codes_to_read) or (not file_cache_is_enough) or (not read_from_file):
        if codes_to_read:
            currencies_cache = get_overall_currencies(list(codes_to_read))
        else:
            currencies_cache = get_overall_currencies(currencies_and_stocks["user_currencies"])
        data_to_write = {}
        if currencies_cache:
            for code, value in currencies_cache['Valute'].items():
                data_to_write[code] = value
            read_from_file.update(data_to_write)

        if read_from_file:
            with open(cache_filename, 'w') as f:
                json.dump(read_from_file, f, indent=4)

    currencies_cache = read_from_file
    return read_from_file


def convert_stocks_prices(from_currency: str = 'USD', to_currency: str = 'RUB') -> None:
    ratio = currencies_cache.get(from_currency)
    if ratio:
        ratio = ratio.get('Value')
        if not ratio:
            return
    else:
        return
    if to_currency != 'RUB':
        ratio2 = currencies_cache.get(to_currency)
        if ratio2:
            ratio2 = ratio2.get('Value')
            if not ratio2:
                return
        ratio /= ratio2

    global stocks_cache
    for stock in stocks_cache:
        stock["price"] = round(ratio * stock["price"], 2)


def convert_to_dict(l: list, key_name: str, value_name: str) -> dict:
    result = {}
    for item in l:
        result[item[key_name]] = item[value_name]
    return result
