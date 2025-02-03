import os
from datetime import datetime as datetime
from json import loads

import src.datetime_utils
import src.views


def test_show_main_page() -> None:
    """
    Тестим работу главной страницы
    полностью (если успеем) мокаем пользовательский ввод, датафрейм и результаты вычислений
    и проверяем, что возвращаемый json-словарь имеет все нужные поля
    """

    # прием взят с https://python.code-maven.com/mocking-input-and-output-for-python-testing
    input_values = ["2021-12-31 11:00:00", "3"]
    output = []

    def mock_input(s):  # мокаем ввод тестового периода
        """Мокаем пользовательский ввод с клавиатуры"""
        output.append(s)
        return input_values.pop(0)

    def mock_dataframe_filename():
        """Мокаем имя файла, откуда будем грузить датафрейм"""
        par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
        par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
        return os.path.join(par_dir, "data", "operations report test.xlsx")

    def content_is_valid(json_str: str) -> bool:
        """
        проверяем содержимое джейсона
        :param json_str: проверяемая стока с данными
        :return: True, если все правильно и все на своем месте
        """
        test_dict = loads(json_str)
        passed = (
            (test_dict.get("greeting") is not None)
            and (test_dict.get("cards") is not None)
            and (test_dict.get("top_transactions") is not None)
            and (test_dict.get("currency_rates") is not None)
            and (test_dict.get("stock_prices") is not None)
        )
        return passed

    src.datetime_utils.input = mock_input
    src.views.print = lambda s: output.append(s)  # если надо, можем посмотреть, что выводилось в консоль
    src.views.get_operations_filename = mock_dataframe_filename

    json_output = src.views.show_main_page()

    assert content_is_valid(json_output)


def test_show_events_page() -> None:
    """
    тестим работу страницы 'события'
    полностью (если успеем) мокаем пользовательский ввод, датафрейм и результаты вычислений
    и проверяем, что возвращаемый json-словарь имеет все нужные поля
    """

    # прием взят с https://python.code-maven.com/mocking-input-and-output-for-python-testing
    input_values = ["12.12.2021", "w"]
    output = []

    def mock_input(s):  # мокаем ввод тестового периода
        output.append(s)
        return input_values.pop(0)

    def mock_get_period():
        return datetime(2024, 12, 1), datetime(2024, 12, 31, 23, 59, 59)

    def mock_get_report_span() -> None:
        return "M"

    def mock_dataframe_filename():
        par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
        par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
        return os.path.join(par_dir, "data", "operations report test.xlsx")

    def content_is_valid(json_str: str) -> bool:
        """
        проверяем содержимое джейсона
        :param json_str: проверяемая стока с данными
        :return: True, если все правильно и все на своем месте
        """
        test_dict = loads(json_str)
        passed = (
            (test_dict.get("expenses") is not None)
            and (test_dict.get("transfers_and_cash") is not None)
            and (test_dict.get("income") is not None)
            and (test_dict.get("currency_rates") is not None)
            and (test_dict.get("stock_prices") is not None)
        )
        return passed

    src.datetime_utils.input = mock_input
    src.datetime_utils.get_period = mock_get_period
    src.views.print = lambda s: output.append(s)
    src.views.get_operations_filename = mock_dataframe_filename
    src.views.get_report_span = mock_get_report_span

    json_output = src.views.show_events_page()

    assert content_is_valid(json_output)


def test_show_investment_page() -> None:
    """
    тестим работу страницы 'сервис', инвесткопилка
    полностью (если успеем) мокаем пользовательский ввод, датафрейм и результаты вычислений
    и проверяем возвращаемый результат
    """

    # прием взят с https://python.code-maven.com/mocking-input-and-output-for-python-testing
    input_values = ["2024-12", "50"]
    output = []

    def mock_input(s):  # мокаем ввод тестового периода
        output.append(s)
        return input_values.pop(0)

    def mock_dataframe_filename():
        par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
        par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
        return os.path.join(par_dir, "data", "operations report test2.xlsx")

    # src.datetime_utils.input = mock_input
    # src.datetime_utils.get_period = mock_get_period
    src.views.input = mock_input
    src.views.print = lambda s: output.append(s)
    src.views.get_operations_filename = mock_dataframe_filename
    # src.views.get_report_span = mock_get_report_span

    savings = src.views.show_investment_page()

    assert savings == 399


def test_show_reports_page() -> None:
    """
    тестим работу страницы 'отчеты', расходы за будни/выходные
    полностью (если успеем) мокаем пользовательский ввод, датафрейм и результаты вычислений
    и проверяем возвращаемый результат
    """
    input_values = ["2024-12-29 00:00:00"]
    output = []

    # прием взят с https://python.code-maven.com/mocking-input-and-output-for-python-testing
    def mock_input(s):  # мокаем ввод тестового периода
        output.append(s)
        return input_values.pop(0)

    def mock_get_date():
        return datetime(2024, 12, 29, 23)
        # return '2024-12-29 00:00:00'

    def mock_dataframe_filename():
        par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
        par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
        return os.path.join(par_dir, "data", "operations report test2.xlsx")

    src.datetime_utils.input = mock_input
    src.datetime_utils.get_date = mock_get_date
    src.views.print = lambda s: output.append(s)
    src.views.get_operations_filename = mock_dataframe_filename

    df = src.views.show_reports_page()
    result_dict = {col: int(row.iloc[0]) for col, row in df.iterrows()}

    expected_result_dict = {"Будни": 1000, "Выходные": 500}

    assert result_dict == expected_result_dict
