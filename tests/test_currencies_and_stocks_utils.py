import copy
import json
import os.path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

import src.currencies_and_stocks_utils


# пример взят из https://www.iditect.com/faq/python/preferred-way-of-patching-multiple-methods-in-python-unit-test.html
@patch("os.path.exists")
@patch("os.path.isfile")
def test_load_currencies_and_stocks_from_json(mock_os_path_exists, mock_os_path_isfile) -> None:
    file_data = """{"user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}"""

    def mock_open_file(filename: str) -> str:
        nonlocal file_data
        return file_data

    mock_os_path_exists.return_value = True
    mock_os_path_isfile.return_value = True
    src.currencies_and_stocks_utils.load_existing_file = mock_open_file

    result = src.currencies_and_stocks_utils.load_currencies_and_stocks_from_json("test.json")
    assert result == json.loads(file_data)


def test_get_currencies_rates(example_user_currencies_fixture: dict) -> None:
    """
    Тестим получение цен на валюты пользователя
    мокаем кэш цен на валюты, получаем набор нужных нам цен и сравниваем с ожидаемым результатом
    :param example_user_currencies_fixture: - фикстура с кодами валют пользователя
    """
    mock_currencies_cache = {"USD": {"Value": 100}, "EUR": {"Value": 110}, "CNY": {"Value": 12}}
    src.currencies_and_stocks_utils.currencies_cache = mock_currencies_cache
    currencies_rates = src.currencies_and_stocks_utils.get_currencies_rates(example_user_currencies_fixture)

    user_currencies = example_user_currencies_fixture.get("user_currencies")
    expected_result = []
    for cur in user_currencies:
        stock_data = {"currency": cur, "rate": mock_currencies_cache[cur]["Value"]}
        expected_result.append(stock_data)
    assert expected_result == currencies_rates


def test_get_stocks_prices(example_user_stocks_fixture: dict) -> None:
    """
    тестим получение цен на акции пользователя
    мокаем кэш цен на валюты и акции, получаем набор нужных нам цен и сравниваем с ожидаемым результатом
    :param example_user_stocks_fixture: - фикстура с кодами акций пользователя
    """
    mock_stocks = {
        "AAPL": 240.0,
        "AMZN": 230.0,
        "GOOGL": 200.0,
        "MSFT": 415.0,
        "TSLA": 400.0,
        "NVDA": 125.0,
        "META": 685.0,
        "AVGO": 215.0,
        "WMT": 99.0,
        "V": 340.0,
    }

    mock_currencies_cache = {"USD": {"Value": 100}}

    src.currencies_and_stocks_utils.stocks_cache = mock_stocks
    src.currencies_and_stocks_utils.currencies_cache = mock_currencies_cache
    src.currencies_and_stocks_utils.convert_stocks_prices()
    stocks_prices = src.currencies_and_stocks_utils.get_stocks_prices(example_user_stocks_fixture)

    user_stocks = example_user_stocks_fixture.get("user_stocks")
    expected_result = []
    for stock in user_stocks:
        stock_data = {"stock": stock, "price": mock_stocks[stock]}
        expected_result.append(stock_data)
    assert expected_result == stocks_prices


@pytest.mark.parametrize(
    "user_inputs, expected_results",
    [
        (
            ["1", "1,2", "*", "ehw4h"],
            [
                {"USD": 100},
                {"USD": 100, "EUR": 105},
                {"USD": 100, "EUR": 105, "CNY": 13},
                {"USD": 100, "EUR": 105, "CNY": 13},
            ],
        )
    ],
)
def test_select_users_currencies(user_inputs: list[str], expected_results: list[dict]) -> None:
    """
    # имитируем выбор валют, проверяем вывод
    :param user_inputs: варианты выбора пользователя кодов валют
    :param expected_results:  - соответствующие ожидаемые результаты
    """
    mock_currencies_cache = {
        "USD": {"Value": 100, "Name": "Доллар"},
        "EUR": {"Value": 105, "Name": "Евро"},
        "CNY": {"Value": 13, "Name": "Юань"},
    }
    input_values = user_inputs
    output = []

    def mock_input(s: str) -> str:  # мокаем ввод тестового периода
        """Мокаем пользовательский ввод с клавиатуры"""
        output.append(s)
        return input_values.pop(0)

    def side_effect_func(cur_code_from: str, cur_code_to: str) -> int | float:
        """Мокаем функцию конвертации валют"""
        data_from = mock_currencies_cache.get(cur_code_from)
        if data_from:
            if cur_code_to == "RUB":
                return data_from.get("Value", 0.0)
            else:
                data_to = mock_currencies_cache.get(cur_code_to)
                if data_to:
                    return data_from.get("Value", 0.0) / data_from.get("Value", 1)
                else:
                    return 0
        else:
            return 0

    mock_get_currency_rate = MagicMock(side_effect=side_effect_func)
    src.currencies_and_stocks_utils.input = mock_input
    src.currencies_and_stocks_utils.currencies_cache = mock_currencies_cache
    src.currencies_and_stocks_utils.get_currency_rate = mock_get_currency_rate
    i = 0
    passed = True
    while input_values:
        result = src.currencies_and_stocks_utils.select_users_currencies()
        passed = passed and (result == expected_results[i])
        if passed:
            i += 1
        else:
            break
    assert passed


def test_show_users_rates() -> None:
    """тестим вывод на экран цен на выбранные валюты"""
    mock_users_currencies = ["USD", "EUR"]
    mock_currencies_cache = {
        "USD": {"Value": 100, "Name": "Доллар"},
        "EUR": {"Value": 105, "Name": "Евро"},
        "CNY": {"Value": 13, "Name": "Юань"},
    }
    output = []
    src.currencies_and_stocks_utils.user_currencies = mock_users_currencies
    src.currencies_and_stocks_utils.currencies_cache = mock_currencies_cache
    src.currencies_and_stocks_utils.print = lambda s: output.append(
        s
    )  # если надо, можем посмотреть, что выводилось в консоль
    src.currencies_and_stocks_utils.show_users_rates(mock_users_currencies, "")
    assert output == ["\n", "1 USD == 100 руб.", "1 EUR == 105 руб.", "\n"]


@pytest.mark.parametrize(
    "user_inputs, expected_results",
    [
        (
            ["AAPL", "NVDA,GOOGL", "*", ""],
            [
                {"AAPL": 24000.0},
                {"NVDA": 12500.0, "GOOGL": 20000.0},
                None,
                None,
            ],
        )
    ],
)
def test_select_users_stocks(user_inputs: list[str], expected_results: list) -> None:
    """
    # мокаем кэш цен акций в долларах и цены на валюты
    # проверяем вывод

    :param user_inputs: варианты выбора пользователя кодов валют
    :param expected_results:  - соответствующие ожидаемые результаты
    """
    mock_stocks = {
        "AAPL": 240.0,
        "AMZN": 230.0,
        "GOOGL": 200.0,
        "MSFT": 415.0,
        "TSLA": 400.0,
        "NVDA": 125.0,
        "META": 685.0,
        "AVGO": 215.0,
        "WMT": 99.0,
        "V": 340.0,
    }

    mock_currencies_cache = {
        "USD": {"Value": 100, "Name": "Доллар"},
        "EUR": {"Value": 105, "Name": "Евро"},
        "CNY": {"Value": 13, "Name": "Юань"},
    }
    input_values = user_inputs
    output = []

    def mock_input(s: str) -> str:  # мокаем ввод тестового периода
        """Мокаем пользовательский ввод с клавиатуры"""
        output.append(s)
        return input_values.pop(0)

    def side_effect_func(cur_code_from: str, cur_code_to: str) -> int | float:
        """Мокаем функцию конвертации валют"""
        data_from = mock_currencies_cache.get(cur_code_from)
        if data_from:
            if cur_code_to == "RUB":
                return data_from.get("Value", 0.0)
            else:
                data_to = mock_currencies_cache.get(cur_code_to)
                if data_to:
                    return data_from.get("Value", 0.0) / data_from.get("Value", 1)
                else:
                    return 0
        else:
            return 0

    def side_effect_func2(stock: str) -> int | float:
        """Мокаем API цен на акции"""
        return mock_stocks.get(stock, 0)

    mock_get_currency_rate = MagicMock(side_effect=side_effect_func)
    mock_get_stock_price = MagicMock(side_effect=side_effect_func2)
    src.currencies_and_stocks_utils.input = mock_input
    src.currencies_and_stocks_utils.currencies_cache = mock_currencies_cache
    src.currencies_and_stocks_utils.stocks_cache = mock_stocks
    src.currencies_and_stocks_utils.get_currency_rate = mock_get_currency_rate
    src.currencies_and_stocks_utils.get_stock_price = mock_get_stock_price
    i = 0
    passed = True
    while input_values:
        result = src.currencies_and_stocks_utils.select_users_stocks()
        passed = passed and (result == expected_results[i])
        if passed:
            i += 1
        else:
            break
    assert passed


def test_save_currencies_and_stocks_to_json() -> None:
    """
    # мокаем содержимое словаря валют и акций пользователя
    # проверяем содержимое сохраненного файла

    """

    mock_user_currencies = {"USD": 100.0, "EUR": 105.0}
    mock_user_stocks = {
        "AAPL": 24000.0,
        "GOOGL": 20000.0,
        "MSFT": 41500.0,
    }

    src.currencies_and_stocks_utils.user_currencies = mock_user_currencies
    src.currencies_and_stocks_utils.user_stocks = mock_user_stocks

    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    test_filename = os.path.join(par_dir, "test_user_settings.json")

    src.currencies_and_stocks_utils.save_currencies_and_stocks_to_json(test_filename)
    passed = os.path.exists(test_filename)
    if passed:
        with open(test_filename, encoding="utf8") as f:
            content = f.read()
            passed = content == '{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL", "MSFT"]}'
    assert passed


def test_cache_stocks() -> None:
    """мокаем кэш цен на акции - заранее неполный
    пополняем его через файл кэша
    проверяем его обновление через апи
    """

    mock_stocks = {
        "GOOGL": 200.0,
        "MSFT": 415.0,
        "TSLA": 400.0,
        "NVDA": 125.0,
        "META": 685.0,
        "AVGO": 215.0,
        "WMT": 99.0,
        "V": 340.0,
    }

    file_data = """[{"symbol": "GOOGL", "price": 191.81}, {"symbol": "MSFT", "price": 434.56}, {"symbol": "TSLA",
    "price": 397.15}] """

    def mock_open_file(filename: str) -> str:
        nonlocal file_data
        return file_data

    def mock_load_currencies_and_stocks(filename: str) -> Any:
        return json.loads("""{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT"]}""")

    old_mock_stocks = copy.deepcopy(mock_stocks)
    src.currencies_and_stocks_utils.stocks_cache = mock_stocks
    src.currencies_and_stocks_utils.load_currencies_and_stocks_from_json = mock_load_currencies_and_stocks
    src.currencies_and_stocks_utils.load_existing_file = mock_open_file
    mock_stocks = src.currencies_and_stocks_utils.cache_stocks(file_cache_is_enough=True)

    # как минимум это должно подгрузиться из файла кэша
    passed = (mock_stocks.get("AAPL") is not None) and (mock_stocks.get("AMZN") is not None)

    if passed:  # проверяем, обновились ли цены
        passed = False
        for stock in mock_stocks:
            old_price = old_mock_stocks.get(stock, 0)
            updated_price = mock_stocks.get(stock, 0)
            passed = old_price != updated_price
            if passed:
                break
    assert passed


def test_cache_currencies() -> None:
    """мокаем кэш цен на валюты - заранее неполный
    пополняем его через файл кэша
    проверяем его обновление через апи
    """
    mock_currencies_cache = {"CNY": {"Value": 13, "Name": "Юань"}}

    file_data = """{    "USD": {
        "ID": "R01235",
        "NumCode": "840",
        "CharCode": "USD",
        "Nominal": 1,
        "Name": "\u0414\u043e\u043b\u043b\u0430\u0440 \u0421\u0428\u0410",
        "Value": 97.9658,
        "Previous": 97.132
    }}"""

    def mock_open_file(filename: str) -> str:
        nonlocal file_data
        return file_data

    def mock_load_currencies_and_stocks(filename: str) -> Any:
        return json.loads("""{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT"]}""")

    old_mock_currencies = copy.deepcopy(mock_currencies_cache)
    src.currencies_and_stocks_utils.currencies_cache = mock_currencies_cache
    src.currencies_and_stocks_utils.load_currencies_and_stocks_from_json = mock_load_currencies_and_stocks
    src.currencies_and_stocks_utils.load_existing_file = mock_open_file
    mock_currencies_cache = src.currencies_and_stocks_utils.cache_currencies(file_cache_is_enough=False)

    # как минимум это должно подгрузиться из файла кэша
    passed = mock_currencies_cache.get("USD") is not None

    if passed:  # проверяем, обновились ли цены
        passed = False
        for stock in mock_currencies_cache:
            old_price = old_mock_currencies.get(stock, 0)
            updated_price = mock_currencies_cache.get(stock, {}).get("Value", 0)
            passed = old_price != updated_price
            if passed:
                break
    assert passed


def test_convert_stocks_prices() -> None:
    """мокаем кэш цен на валюты и акции
    # проверяем конвертацию из долларов в рубли
    """
    mock_currencies_cache = {
        "USD": {"Value": 100, "Name": "Доллар"},
        "EUR": {"Value": 105, "Name": "Евро"},
        "CNY": {"Value": 13, "Name": "Юань"},
    }

    mock_stocks = {"AAPL": 240.0, "AMZN": 230.0}

    src.currencies_and_stocks_utils.currencies_cache = mock_currencies_cache
    src.currencies_and_stocks_utils.stocks_cache = mock_stocks

    src.currencies_and_stocks_utils.convert_stocks_prices(from_currency="USD", to_currency="RUB")
    assert mock_stocks == {"AAPL": 24000.0, "AMZN": 23000.0}


def test_convert_to_dict() -> None:
    """проверяем перевод списка в словарь"""
    test_list = [
        {"symbol": "GOOGL", "price": 191.81},
        {"symbol": "MSFT", "price": 434.56},
        {"symbol": "TSLA", "price": 397.15},
        {"symbol": "AMZN", "price": 237.68},
        {"symbol": "AAPL", "price": 236.0},
    ]
    expected_result = {"GOOGL": 191.81, "MSFT": 434.56, "TSLA": 397.15, "AMZN": 237.68, "AAPL": 236.0}
    result = src.currencies_and_stocks_utils.convert_to_dict(test_list, "symbol", "price")
    assert expected_result == result
