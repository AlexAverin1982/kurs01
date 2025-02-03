import unittest
from datetime import datetime as datetime

import pytest

from src.datetime_utils import get_date, get_month_dates, get_period, get_report_span, get_span_dates, is_leap_year


@pytest.mark.parametrize("test_years, expected", [([1900, 1999, 2000, 2004], [False, False, True, True])])
def test_is_leap_year(test_years: list[int], expected: list[bool]) -> None:
    # используем параметризацию
    passed = True
    for i, year in enumerate(test_years):
        passed = passed and (is_leap_year(year) == expected[i])
    assert passed


def test_get_date() -> None:
    """
    мокаем пользовательский ввод, проверяем дату на выходе
    def test_function():
        with mock.patch.object(__builtins__, 'input', lambda: 'some_input'):
            assert module.function() == 'expected_output'
    """
    with unittest.mock.patch("builtins.input", return_value="1.12.2005"):
        assert get_date(format_string="%d.%m.%Y") == datetime(2005, 12, 1)


@pytest.mark.parametrize(
    "end_date, expected_result", [(["2019-07-15 00:00:00"], (datetime(2019, 7, 1), datetime(2019, 7, 15)))]
)
def test_get_period(end_date, expected_result) -> None:
    """Мокаем пользовательский ввод, проверяем даты на выходе"""
    with unittest.mock.patch("builtins.input", return_value=end_date[0]):
        assert get_period() == expected_result


@pytest.mark.parametrize(
    "user_inputs, expected_outputs",
    [
        (
            [
                "w",
                "m",
                "y",
                "all",
            ],
            [
                "W",
                "M",
                "Y",
                "ALL",
            ],
        )
    ],
)
def test_get_report_span(user_inputs, expected_outputs) -> None:
    # мокаем все возможные варианты ввода и проверяем возврат
    outputs = []
    for mock_input in user_inputs:
        with unittest.mock.patch("builtins.input", return_value=mock_input):
            outputs.append(get_report_span())
    assert outputs == expected_outputs

    assert True


@pytest.mark.parametrize(
    "test_input_dates, periods, expected_spans",
    [
        (
            [
                datetime(2021, 12, 1),
                datetime(2021, 11, 21),
                datetime(2020, 10, 14),
                datetime(2021, 12, 1),
                datetime(2020, 2, 28),
            ],
            ["W", "M", "Y", "ALL", ""],
            [
                (datetime(2021, 11, 29, 0, 0), datetime(2021, 12, 5, 23, 59, 59)),
                (datetime(2021, 11, 1, 0, 0), datetime(2021, 11, 30, 23, 59, 59)),
                (datetime(2020, 1, 1, 0, 0), datetime(2020, 12, 31, 23, 59, 59)),
                (datetime(1900, 1, 1, 0, 0), datetime(2021, 12, 1, 23, 59, 59)),
                (datetime(2020, 2, 1, 0, 0), datetime(2020, 2, 29, 23, 59, 59)),
            ],
        )
    ],
)
def test_get_span_dates(test_input_dates, periods, expected_spans) -> None:
    passed = True
    for i, test_date in enumerate(test_input_dates):
        result = get_span_dates(test_date, periods[i])
        passed = passed and (result == expected_spans[i])
    assert passed


@pytest.mark.parametrize(
    "test_input_dates, expected_spans",
    [
        (
            ["2019-11", "2020-02", "1900-02"],
            [
                (datetime(2019, 11, 1, 0, 0), datetime(2019, 11, 30, 23, 59, 59)),
                (datetime(2020, 2, 1, 0, 0), datetime(2020, 2, 29, 23, 59, 59)),
                (datetime(1900, 2, 1, 0, 0), datetime(1900, 2, 28, 23, 59, 59)),
            ],
        )
    ],
)
def test_get_month_dates(test_input_dates, expected_spans) -> None:
    passed = True
    for i, test_date in enumerate(test_input_dates):
        result = get_month_dates(test_date)
        passed = passed and (result == expected_spans[i])
    assert passed
