import os
from datetime import datetime as datetime

import pytest

from src.utils import (
    convert_dataframe_to_listdict,
    convert_values_in_listdict,
    filter_operations_by_period,
    get_cards_totals,
    get_dataframe_from_xlsx,
    get_operations_totals,
    get_top_operations,
    get_top_transactions,
    greet_user,
)


@pytest.mark.parametrize(
    "test_datetimes, expected_greetings",
    [
        (
            [
                datetime(2025, 1, 1),
                datetime(2025, 1, 1, 6, 30),
                datetime(2025, 1, 1, 13, 45),
                datetime(2025, 1, 1, 17, 30),
                datetime(2025, 1, 1, 23),
            ],
            ["Доброй ночи", "Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"],
        )
    ],
)
def test_greet_user(test_datetimes, expected_greetings) -> None:
    passed = True
    for i, test_datetime in enumerate(test_datetimes):
        passed = passed and (greet_user(test_datetime) == expected_greetings[i])
    assert passed


def test_get_dataframe_from_xlsx(test_dataframe_as_list: list[list]) -> None:
    """
    грузим тестовый датафрейм, заранее зная, что там
    преобразуем в список словарей строк,
    сопоставляем с ожидаемым содержимым
    """
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations report test.xlsx")
    dataframe = get_dataframe_from_xlsx(filename)
    # для простоты конвертируем некоторые столбцы
    dataframe["Дата операции"] = dataframe["Дата операции"].astype("str")
    dataframe["Дата платежа"] = dataframe["Дата платежа"].astype("str")
    dataframe["MCC"] = dataframe["MCC"].fillna(value=0)
    dataframe["MCC"] = dataframe["MCC"].astype("int")

    result_list = []

    for col, row in dataframe.iterrows():
        row_list = [row.iloc[i] for i in range(len(row))]
        result_list.append(row_list)

    assert test_dataframe_as_list == result_list


def test_filter_operations_by_period(test_dataframe_as_list2: list[list]) -> None:
    """
    грузим тестовый датафрейм, заранее зная, что там,
    фильтруем период, фильтруем доход/расход
    преобразуем в список словарей строк,
    сопоставляем с ожидаемым содержимым
    """
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations report test2.xlsx")
    dataframe = get_dataframe_from_xlsx(filename)
    # для простоты конвертируем некоторые столбцы
    dataframe["Дата операции"] = dataframe["Дата операции"].astype("str")

    dataframe["MCC"] = dataframe["MCC"].fillna(value=0)
    dataframe["MCC"] = dataframe["MCC"].astype("int")

    # фильтруем по периоду и расходам
    df_filtered_by_period = filter_operations_by_period(
        dataframe=dataframe,
        period_column="Дата платежа",
        period_start=datetime(2024, 12, 30),
        period_end=datetime(2024, 12, 30, 1),
        expenses_column="Сумма платежа",
        filter_expenses=True,
    )

    df_filtered_by_period["Дата платежа"] = df_filtered_by_period["Дата платежа"].astype("str")

    result_list = []
    for col, row in df_filtered_by_period.iterrows():
        row_list = [row.iloc[i] for i in range(len(row))]
        result_list.append(row_list)

    assert [test_dataframe_as_list2[0]] == result_list


def test_get_cards_totals(test_dataframe_as_list: list[list]) -> None:
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations report test2.xlsx")
    dataframe = get_dataframe_from_xlsx(filename)
    # для простоты конвертируем некоторые столбцы
    dataframe["Дата операции"] = dataframe["Дата операции"].astype("str")

    dataframe["MCC"] = dataframe["MCC"].fillna(value=0)
    dataframe["MCC"] = dataframe["MCC"].astype("int")

    # фильтруем по периоду и расходам
    df_filtered_by_period = filter_operations_by_period(
        dataframe=dataframe,
        period_column="Дата платежа",
        period_start=datetime(2024, 12, 1),
        period_end=datetime(2025, 1, 1),
        expenses_column="Сумма платежа",
        filter_expenses=True,
    )

    cards_totals = get_cards_totals(
        dataframe=df_filtered_by_period,
        card_no_column="Номер карты",
        payment_column="Сумма платежа",
        cashback_column="Кэшбэк",
    )

    expected_result = [
        {"last_digits": "5091", "total_spent": 2000, "cashback": 3},
        {"last_digits": "7197", "total_spent": 4001, "cashback": 5},
    ]

    assert cards_totals == expected_result


def test_get_top_transactions(test_dataframe_as_list3: list[list]) -> None:
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations report test3.xlsx")
    dataframe = get_dataframe_from_xlsx(filename)
    # для простоты конвертируем некоторые столбцы
    dataframe["Дата операции"] = dataframe["Дата операции"].astype("str")

    dataframe["MCC"] = dataframe["MCC"].fillna(value=0)
    dataframe["MCC"] = dataframe["MCC"].astype("int")

    top_transactions = get_top_transactions(
        dataframe=dataframe,
        transactions_count=6,
        payment_column="Сумма платежа",
        period_column="Дата платежа",
        date_format="%d.%m.%Y",
        category_column="Категория",
        description_column="Описание",
    )

    expect_result = [
        {"date": "27.12.2024", "amount": 6, "category": "Категория_6", "description": "Колхоз"},
        {"date": "26.12.2024", "amount": 5, "category": "Категория_5", "description": "Колхоз"},
        {"date": "25.12.2024", "amount": 4, "category": "Категория_4", "description": "Колхоз"},
        {"date": "24.12.2024", "amount": 3, "category": "Категория_3", "description": "Колхоз"},
        {"date": "23.12.2024", "amount": 2, "category": "Категория_2", "description": "Колхоз"},
        {"date": "30.12.2024", "amount": 1, "category": "Категория_1", "description": "Колхоз"},
    ]

    assert top_transactions == expect_result


def test_get_operations_totals(test_dataframe_as_list3: list[list]) -> None:
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations report test3.xlsx")
    dataframe = get_dataframe_from_xlsx(filename)
    # для простоты конвертируем некоторые столбцы
    dataframe["Дата операции"] = dataframe["Дата операции"].astype("str")

    dataframe["MCC"] = dataframe["MCC"].fillna(value=0)
    dataframe["MCC"] = dataframe["MCC"].astype("int")

    result = get_operations_totals(dataframe=dataframe, payment_column="Сумма платежа")
    assert result == 21.0


def test_get_top_operations(test_dataframe_as_list3: list[list]) -> None:
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations report test3.xlsx")
    dataframe = get_dataframe_from_xlsx(filename)
    # для простоты конвертируем некоторые столбцы
    dataframe["Дата операции"] = dataframe["Дата операции"].astype("str")

    dataframe["MCC"] = dataframe["MCC"].fillna(value=0)
    dataframe["MCC"] = dataframe["MCC"].astype("int")

    result = get_top_operations(
        dataframe=dataframe, payment_column="Сумма платежа", category_column="Категория", categories_count=3
    )

    # -> tuple[int, list[dict]]

    assert result == (
        15,
        [
            {"category": "Категория_6", "amount": 6},
            {"category": "Категория_5", "amount": 5},
            {"category": "Категория_4", "amount": 4},
        ],
    )


def test_convert_dataframe_to_listdict(test_dataframe_as_list3: list[list]) -> None:
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations report test3.xlsx")
    dataframe = get_dataframe_from_xlsx(filename)
    # для простоты конвертируем некоторые столбцы
    dataframe["Дата операции"] = dataframe["Дата операции"].astype("str")
    dataframe["Дата платежа"] = dataframe["Дата платежа"].astype("str")

    dataframe["MCC"] = dataframe["MCC"].fillna(value=0)
    dataframe["MCC"] = dataframe["MCC"].astype("int")

    dataframe = dataframe.head(1)

    result = convert_dataframe_to_listdict(dataframe)
    expected_result = [
        {
            "Дата операции": "2024-12-30",
            "Дата платежа": "2024-12-30",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -1,
            "Валюта операции": "RUB",
            "Сумма платежа": -1,
            "Валюта платежа": "RUB",
            "Кэшбэк": 1,
            "Категория": "Категория_1",
            "MCC": 5411,
            "Описание": "Колхоз",
        }
    ]
    assert expected_result == result


def test_convert_values_in_listdict(test_dataframe_as_list3: list[list]) -> None:
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations report test3.xlsx")
    dataframe = get_dataframe_from_xlsx(filename)
    # для простоты конвертируем некоторые столбцы
    dataframe["Дата операции"] = dataframe["Дата операции"].astype("str")
    dataframe["Дата платежа"] = dataframe["Дата платежа"].astype("str")

    dataframe["MCC"] = dataframe["MCC"].fillna(value=0)
    dataframe["MCC"] = dataframe["MCC"].astype("int")

    # dataframe = dataframe.head(1)

    listdict = convert_dataframe_to_listdict(dataframe)
    convert_values_in_listdict(
        listdict=listdict, key_name="Дата операции", convert_to_type=datetime, format_str="%Y-%m-%d"
    )

    passed = True
    for item in listdict:
        passed = passed and isinstance(item["Дата операции"], datetime)

    assert passed
