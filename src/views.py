import os.path
from json import dumps
from operator import itemgetter
from re import match

from pandas import DataFrame

from src.currencies_and_stocks_utils import (
    get_currencies_rates,
    get_stocks_prices,
    load_currencies_and_stocks_from_json,
)
from src.datetime_utils import get_date, get_period, get_report_span, get_span_dates
from src.reports import spending_by_workday
from src.services import investment_bank
from src.utils import (
    convert_dataframe_to_listdict,
    filter_operations_by_period,
    get_cards_totals,
    get_dataframe_from_xlsx,
    get_operations_totals,
    get_top_operations,
    get_top_transactions,
    greet_user,
)

par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))


def get_operations_filename() -> str:
    """
    Written specially for mocking purposes...
    :return: filename to read dataframe from
    """
    global par_dir
    return os.path.join(par_dir, "data", "operations.xlsx")


def show_main_page() -> str:
    """JSON-данные по баноковским операциям на главной web-странице"""
    global par_dir
    # приветствие
    result = {"greeting": greet_user()}

    # грузим данные из xlsx
    filename = get_operations_filename()
    dataframe = get_dataframe_from_xlsx(filename)

    # запрашиваем отчетный период
    report_date_start, report_date_end = get_period()
    # date_format = '%d.%m.%Y'
    # date_format = 'YYYY-MM-DD HH:MM:SS'
    # report_date_start = str(report_date_start)
    # report_date_end = str(report_date_end)

    # report_date_start = '01.12.2021'
    # report_date_end = '19.12.2021'

    # фильтруем траты по периоду
    df_period_filtered = filter_operations_by_period(
        dataframe=dataframe,
        period_column="Дата платежа",
        period_start=report_date_start,
        period_end=report_date_end,
        # date_format=date_format,
        expenses_column="Сумма платежа",
    )

    # получаем сводные данные по картам
    result["cards"] = get_cards_totals(
        dataframe=df_period_filtered,
        card_no_column="Номер карты",
        payment_column="Сумма платежа",
        cashback_column="Кэшбэк",
    )

    result["top_transactions"] = get_top_transactions(
        dataframe=df_period_filtered,
        transactions_count=5,
        payment_column="Сумма платежа",
        period_column="Дата платежа",
        date_format="%d.%m.%Y",
        category_column="Категория",
        description_column="Описание",
    )

    filename = os.path.join(par_dir, "user_settings.json")

    currencies_and_stocks = load_currencies_and_stocks_from_json(filename)

    result["currency_rates"] = get_currencies_rates(currencies_and_stocks)
    result["stock_prices"] = get_stocks_prices(currencies_and_stocks)

    return dumps(result, ensure_ascii=False, indent=4)


def show_events_page() -> str:
    """JSON-данные по баноковским операциям на web-странице События"""
    result = {}
    global par_dir
    user_filename = os.path.join(par_dir, "user_settings.json")
    currencies_and_stocks = load_currencies_and_stocks_from_json(user_filename)

    # грузим данные из xlsx
    filename = get_operations_filename()
    dataframe = get_dataframe_from_xlsx(filename)

    # запрашиваем дату периода
    report_date_start, report_date_end = get_period("DD.MM.YYYY", prompt="Введите дату из отчетного периода: ")
    # запрос диапазона данных или выбор за месяц указанной даты
    report_span = get_report_span()
    report_date_start, report_date_end = get_span_dates(report_date_end, report_span)
    # ----------------------------------------- расходы ---------------------------------------------------------
    # фильтруем траты по периоду
    # date_format = '%d.%m.%Y'
    df_period_filtered = filter_operations_by_period(
        dataframe=dataframe,
        period_column="Дата платежа",
        period_start=report_date_start,
        period_end=report_date_end,
        # date_format=date_format,
        expenses_column="Сумма платежа",
    )
    # сумма расходов за период
    total_expenses = get_operations_totals(dataframe=df_period_filtered, payment_column="Сумма платежа")
    total_expenses = int(round(abs(total_expenses), 0))
    # группируем расходы по категориям, выбираем 7 самых затратных категорий, остальные суммируем
    main_expenses_data = get_top_operations(
        dataframe=df_period_filtered, categories_count=7, payment_column="Сумма платежа", category_column="Категория"
    )
    rest = {"category": "Остальное", "amount": total_expenses - main_expenses_data[0]}
    main_expenses_data[1].append(rest)
    result["expenses"] = {"total_amount": total_expenses, "main": main_expenses_data[1]}

    # отдельно суммируем расходы на переводы и обнал
    df_transfers_and_cash = df_period_filtered[
        (df_period_filtered["Категория"] == "Переводы") | (df_period_filtered["Категория"] == "Наличные")
    ]

    transfers_and_cash = get_top_operations(
        dataframe=df_transfers_and_cash,
        categories_count=2,
        payment_column="Сумма платежа",
        category_column="Категория",
    )[1]

    result["transfers_and_cash"] = sorted(transfers_and_cash, key=itemgetter("amount"), reverse=True)
    # ----------------------------------------- доходы ---------------------------------------------------------
    df_period_filtered = filter_operations_by_period(
        dataframe=dataframe,
        period_column="Дата платежа",
        period_start=report_date_start,
        period_end=report_date_end,
        # date_format=date_format,
        expenses_column="Сумма платежа",
        filter_expenses=False,
    )
    # группируем приход по категориям
    income_categories_data = get_top_operations(
        dataframe=df_period_filtered, payment_column="Сумма платежа", category_column="Категория"
    )

    # total_income = get_operations_totals(dataframe=df_period_filtered, payment_column='Сумма платежа')
    result["income"] = {
        "total_amount": income_categories_data[0],
        "main": sorted(income_categories_data[1], key=itemgetter("amount"), reverse=True),
    }

    # валюты и акции
    result["currency_rates"] = get_currencies_rates(currencies_and_stocks)
    result["stock_prices"] = get_stocks_prices(currencies_and_stocks)

    return dumps(result, ensure_ascii=False, indent=4)


def show_investment_page() -> float:
    """Страница Сервис - инвесткопилка"""

    def date_is_invalid(date: str) -> bool:
        """Проверяем корректность ввода месяца"""
        return match(r"^(19|20)\d{2}-(0[1-9]|1[012])$", date, flags=0) is None

    month = "2021-12"
    limit = 100
    invalid_input = True
    while invalid_input:
        month = input("Введите месяц в формате YYYY-MM: ")
        invalid_input = date_is_invalid(month)

    global par_dir

    print("Инвесткопилка позволяет копить через округление ваших трат.")
    print("Можно задать комфортный порог округления: 10, 50 или 100 ₽.")
    print("Траты будут округляться, и разница между фактической суммой трат по карте")
    print("и суммой округления будет попадать на счет «Инвесткопилки».")

    invalid_input = True
    while invalid_input:
        limit = input("Введите целую сумму порога округления: ")
        if limit.isdigit():
            limit = int(limit)
            invalid_input = False
        else:
            print("\nОшибочный ввод. Порог - это целое число.\n")

    print("Считаем...")
    # грузим данные из xlsx
    filename = get_operations_filename()
    dataframe = get_dataframe_from_xlsx(filename)
    transactions = convert_dataframe_to_listdict(dataframe)

    savings = investment_bank(month, transactions, limit)
    print(f"Инвесткопилка за месяц {month} с порогом округления {limit} могла бы пополниться на сумму {savings} руб.")
    return savings


def show_reports_page() -> DataFrame:
    """Страница отчетов: средние расходы по выходным и будням за 3 месяца"""
    period_end = get_date(format_string="%Y-%m-%d %H:%M:%S")
    global par_dir
    filename = get_operations_filename()
    dataframe = get_dataframe_from_xlsx(filename)
    return spending_by_workday(dataframe, str(period_end))
