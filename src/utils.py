import datetime as dt
import os
import json
import time
from datetime import datetime as datetime
from datetime import timedelta as tdelta
from time import strptime, strftime, struct_time
from pandas import read_excel, DataFrame, to_datetime
from time import mktime
from math import isnan


def greet_user(current_time: datetime = datetime.now()):
    """ Строка приветствия пользователя, различающаяся в зависимости от времени суток """
    if current_time.hour * 60 + current_time.minute < 340:
        result = "Доброй ночи"
    elif current_time.hour * 60 + current_time.minute < 12 * 60:
        result = "Доброе утро"
    elif current_time.hour * 60 + current_time.minute < 17 * 60:
        result = "Добрый день"
    elif current_time.hour * 60 + current_time.minute < 22 * 60:
        result = "Добрый вечер"
    else:
        result = "Доброй ночи"
    return result


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

def get_dataframe_from_xlsx(filepath: str) -> DataFrame:
    """ Загружает данные по транзакциям из файлов excel """
    return read_excel(filepath)


def filter_operations_by_period(dataframe: DataFrame, period_column: str, period_start: datetime, period_end: datetime,
                                expenses_column: str, filter_expenses: bool = True) -> DataFrame:
    """ Фильтруем dataframe: берем только отчетный период и только траты (платеж меньше нуля)
    или только приход"""

    # convert date column into date format
    # report_date_start = datetime.strftime('%Y-%m-%d', strptime(period_start, date_format))
    # report_date_end = datetime.strftime('%Y-%m-%d', strptime(period_end, date_format))

    report_date_start = period_start
    report_date_end = period_end

    dataframe[period_column] = to_datetime(dataframe[period_column], dayfirst=True)

    df_period_filtered = dataframe[
        (dataframe[period_column] >= report_date_start) & (dataframe[period_column] <= report_date_end)]

    if filter_expenses:
        df_period_filtered = df_period_filtered[df_period_filtered[expenses_column] < 0]
    else:
        df_period_filtered = df_period_filtered[df_period_filtered[expenses_column] > 0]

    return df_period_filtered.sort_values(by=period_column)


def get_cards_totals(dataframe: DataFrame, card_no_column: str,
                     payment_column: str, cashback_column: str) -> list[dict]:
    """ Сводные данные по картам: сумма трат и кэшбэка """
    # группируем по номерам банковских карт
    df_grouped_by_cards = dataframe.groupby(by=card_no_column)
    agg_rule = {payment_column: 'sum', cashback_column: 'sum'}
    totals_by_cards = df_grouped_by_cards.agg(agg_rule)  # returns dataframe

    totals_by_cards.reset_index()  # make sure indexes pair with number of rows
    cards_data = []
    for card_no, row in totals_by_cards.iterrows():
        card_totals = {"last_digits": card_no[1:],
                       "total_spent": round(float(abs(row[payment_column])), 2),
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
                       "amount": round(float(abs(row[payment_column])), 2),
                       # "amount": "%.02f" % float(-row[payment_column]),
                       "category": row[category_column],
                       "description": row[description_column]}
        top_transactions.append(transaction)

    return top_transactions


def get_operations_totals(dataframe: DataFrame, payment_column: str) -> float:
    """ Сводные данные по картам: сумма трат и кэшбэка """
    totals = dataframe.agg({payment_column: 'sum'})  # returns dataframe
    return float(abs(totals.iloc[0]))


def get_top_operations(dataframe: DataFrame, payment_column: str, category_column: str,
                       categories_count: int = 0) -> tuple[int, list[dict]]:
    """ Топ расходов по категориям """
    # группируем по категориям, суммируя расходы

    """ 
    df_grouped_by_cards = dataframe.groupby(by=card_no_column)
    agg_rule = {payment_column: 'sum', cashback_column: 'sum'}
    totals_by_cards = df_grouped_by_cards.agg(agg_rule)  # returns dataframe
    
    """

    agg_expenses_grouped_by_category = dataframe.groupby(by=category_column).agg({payment_column: 'sum'})
    # сортируем итоговые траты по убыванию
    if categories_count:
        expenses_top = agg_expenses_grouped_by_category.nsmallest(categories_count, columns=payment_column)
    else:
        expenses_top = agg_expenses_grouped_by_category

    top_expenses = []
    total_expenses = 0
    for category, expense in expenses_top.iterrows():
        expense = {"category": category, "amount": int(round(abs(expense.iloc[0]), 0))}
        total_expenses += expense["amount"]
        top_expenses.append(expense)

    return total_expenses, top_expenses


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

def convert_dataframe_to_listdict(df: DataFrame) -> list[dict]:
    """ Преобразует датафрейм в список словарей (не знаю, зачем) """
    result = []
    fields = list(df.head(0).columns.values)
    for i in range(df.shape[0]):
        row = list(df.iloc[i])
        result.append(dict(zip(fields, row)))
    return result


def convert_values_in_listdict(listdict: list[dict], key_name: str,
                               convert_to_type: type, format_str: str = '') -> None:
    """ Преобразует значение укзаанного поля всех словарей списка к указанному типу """

    for d in listdict:
        src_value = d.get(key_name)
        if not src_value:
            continue
        if convert_to_type is datetime:
            d[key_name] = datetime.fromtimestamp(mktime(strptime(str(src_value), format_str)))
        else:
            d[key_name] = convert_to_type(src_value)
