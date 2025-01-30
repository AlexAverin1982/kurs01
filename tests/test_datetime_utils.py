import unittest

import pytest
from unittest.mock import Mock, patch

from src.datetime_utils import is_leap_year, get_date
from datetime import datetime as datetime


@pytest.mark.parametrize(
    "test_years, expected",
    [([1900, 1999, 2000, 2004],
      [False, False, True, True])])
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
    with unittest.mock.patch('builtins.input', return_value='1.12.2005'):
        assert get_date(format_string="%d.%m.%Y") == datetime(2005, 12, 1)


def test_get_period() -> None:
    assert True


def test_get_report_span() -> None:
    assert True


def test_get_span_dates() -> None:
    assert True


def test_get_month_dates() -> None:
    assert True
