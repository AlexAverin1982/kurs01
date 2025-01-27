import datetime as dt
import os
import json
from datetime import datetime as datetime
from time import strptime, strftime
from pandas import read_excel, DataFrame, to_datetime
from math import isnan

from src.external_api import get_currency_rate

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


def show_main_page_menu() -> int:
    while True:
        print('-' * 20 + ' Главная страница ' + '-' * 20)
        print('Выберите дальнейшее действие: ')
        print('1. Отобразить статистику по банковским операциям')
        print('2. Информация о валютах и акциях')
        print('99. Выход')
        user_input = input('\nВаш выбор: ')
        if user_input.isdigit():
            break
    return int(user_input)


def greet_user(time: datetime = datetime.now()):
    """ Строка приветствия пользователя, различающаяся в зависимости от времени суток """
    if time.hour * 60 + time.minute < 340:
        result = "Доброй ночи"
    elif time.hour * 60 + time.minute < 12 * 60:
        result = "Доброе утро"
    elif time.hour * 60 + time.minute < 17 * 60:
        result = "Добрый день"
    elif time.hour * 60 + time.minute < 22 * 60:
        result = "Добрый вечер"
    else:
        result = "Доброй ночи"
    return result


def get_period() -> tuple[datetime, datetime]:
    """ Запрашиваем у пользователя конечную дату отчетного периода
    и возвращаем начало и конец периода"""
    date_format = 'YYYY-MM-DD HH:MM:SS'
    correct_input = False
    period_start = period_end = datetime.now()
    while not correct_input:
        try:
            print(f'Корректный формат ввода даты: {date_format}\n')
            period_end = input("Введите дату конца отчетного периода:")
            period_end = strptime(period_end, '%Y-%m-%d %H:%M:%S')
            correct_input = True
            period_start = datetime(period_end.tm_year, period_end.tm_mon, 1)
        except:
            print('Неверный формат ввода даты.\n')

    return period_start, period_end


def get_dataframe_from_xlsx(filepath: str) -> DataFrame:
    """ Загружает данные по транзакциям из файлов excel """
    return read_excel(filepath)


# def load_ops_from_xlsx(filepath: str) -> list[dict]:
#     """загружает данные по транзакциям из файлов excel"""
#     result = []
#     try:
#         # column_types = {'id': int, 'state': str, 'date': datetime, 'amount': int,
#         #                 'currency_name': str, 'currency_code':str, 'from': str, 'to': str, 'description': str}
#         excel_data = read_excel(filepath, dtype=str)
#         fields = list(excel_data.head(0).columns.values)
#         for i in range(excel_data.shape[0]):
#             row = list(excel_data.iloc[i])
#             result.append(dict(zip(fields, row)))
#     except:
#         result = []
#
#     return result


def filter_expenses_by_period(dataframe: DataFrame, period_column: str, period_start: str, period_end: str,
                              date_format: str, expenses_column: str) -> DataFrame:
    """ Фильтруем dataframe: берем только отчетный период и только траты (платеж меньше нуля) """

    # convert date column into date format
    report_date_start = strftime('%Y-%m-%d', strptime(period_start, date_format))
    report_date_end = strftime('%Y-%m-%d', strptime(period_end, date_format))

    dataframe[period_column] = to_datetime(dataframe[period_column], dayfirst=True)

    df_period_filtered = dataframe[
        (dataframe[period_column] >= report_date_start) & (dataframe[period_column] <= report_date_end)]

    df_period_filtered = df_period_filtered[df_period_filtered[expenses_column] < 0]

    return df_period_filtered.sort_values(by=period_column)


def get_cards_totals(dataframe: DataFrame, card_no_column: str, payment_column: str, cashback_column: str) -> DataFrame:
    """ Сводные данные по картам: сумма трат и кэшбэка """
    # группируем по номерам банковских карт
    df_grouped_by_cards = dataframe.groupby(by=card_no_column)
    agg_rule = {payment_column: 'sum', cashback_column: 'sum'}
    totals_by_cards = df_grouped_by_cards.agg(agg_rule)  # returns dataframe

    totals_by_cards.reset_index()  # make sure indexes pair with number of rows
    cards_data = []
    for card_no, row in totals_by_cards.iterrows():
        card_totals = {"last_digits": card_no[1:],
                       "total_spent": round(float(-row[payment_column]), 2),
                       "cashback": round(float(row[cashback_column]), 2)}
        cards_data.append(card_totals)

    return cards_data


def get_top_transactions(dataframe: DataFrame, transactions_count: int, payment_column: str, period_column: str,
                         date_format: str, category_column: str, description_column: str) -> list[dict]:
    """ Топ транзакций """
    # сортируем исходные траты по убыванию
    transactions_top = dataframe[payment_column].nsmallest(transactions_count)

    top_transactions = []
    for row_index in transactions_top.index:
        row = dataframe.loc[row_index]
        transaction = {"date": row[period_column].strftime(date_format),
                       "amount": round(float(-row[payment_column]), 2),
                       # "amount": "%.02f" % float(-row[payment_column]),
                       "category": row[category_column],
                       "description": row[description_column]}
        top_transactions.append(transaction)

    return top_transactions


def load_currencies_and_stocks_from_json(filename: str) -> list[dict]:
    """ Функция принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о курсах валют и стоимости акций"""
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
    result = []
    for currency_code in data.get('user_currencies', []):
        currency = {"currency": get_currency_rate(currency_code, 'RUB')}
    return result


def set_users_currencies() -> dict:
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
                           i+1 in indices}
    else:
        print('Выбран основной набор валют: USD, EUR, CNY')
        user_currencies = {code: get_currency_rate(code, 'RUB') for code in ['USD', 'EUR', 'CNY']}

    return user_currencies
# def get_stats_from_list(data_list: list, report_date_start: str, report_date_end: str) -> dict:
#     stats = {}
#
#     date_start = None
#     date_end = None
#
#     report_date_start = strptime(report_date_start, '%d.%m.%Y')
#     report_date_end = strptime(report_date_end, '%d.%m.%Y')
#
#     for item in data_list:
#         payment_sum = float(item.get('Сумма платежа', 0))
#         if payment_sum >= 0:
#             continue
#
#         card_number = item.get('Номер карты', '')
#         if not card_number or not isinstance(card_number, str):
#             continue
#
#         payment_date = item.get('Дата платежа')
#         if payment_date:
#             payment_date = strptime(payment_date, '%d.%m.%Y')
#
#             if not (report_date_start <= payment_date <= report_date_end):
#                 continue
#
#             if date_start:
#                 if payment_date < date_start:
#                     date_start = payment_date
#             else:
#                 date_start = payment_date
#
#             if date_end:
#                 if payment_date > date_end:
#                     date_end = payment_date
#             else:
#                 date_end = payment_date
#
#         totals = stats.get(card_number)
#
#         if totals:
#             balance = totals.get('balance')
#             if balance:
#                 totals['balance'] = balance + payment_sum
#         else:
#             totals = {'balance': payment_sum}
#
#         cashback = float(item.get('Кэшбэк', 0))
#         if isnan(cashback):
#             cashback = 0.0
#
#         total_cashback = totals.get('cashback', 0)
#         totals['cashback'] = total_cashback + cashback
#         stats[card_number] = totals
#
#     return stats
