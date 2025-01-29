from pandas import DataFrame
from typing import Optional
from datetime import datetime as datetime
from datetime import timedelta as tdelta
from decorators import log

from src.utils import filter_operations_by_period


@log(r'..\logs\log1.log')
def spending_by_workday(transactions: DataFrame, date: Optional[str] = None) -> DataFrame:
    """
    :param transactions: датафрейм с транзакциями.
    :param date: Опциональная дата. Если дата не передана, то берется текущая дата.
    :return: Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты).
    """
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    # формируем даты трехмесячного периода
    date_start = date_end = date + tdelta(days=1) - tdelta(seconds=1)
    month = date_end.month
    if month < 4:
        month += 9
        year = date_end.year - 1
    else:
        month -= 3
        year = date_end.year
    valid_date = False
    day = date_end.day
    while not valid_date:
        try:
            date_start = datetime(year, month, day)
            valid_date = True
        except ValueError:
            day -= 1
    # фильтруем датафрейм по периоду
    df_period_filtered = filter_operations_by_period(dataframe=transactions,
                                                     period_column='Дата платежа',
                                                     period_start=date_start,
                                                     period_end=date_end,
                                                     # date_format=date_format,
                                                     expenses_column='Сумма платежа')
    # добавляем столбец с признаком выходного дня даты платежа
    df_period_filtered.insert(loc=0, column="Дни", value='')
    # df_period_filtered["Выходной"] = datetime.weekday(df_period_filtered['Дата платежа'])
    df_period_filtered["Дни"] = (df_period_filtered["Дата платежа"].apply(datetime.weekday) == 5) | (
            df_period_filtered["Дата платежа"].apply(datetime.weekday) == 6)
    # вычисляем средние траты по выходным и по будням

    df_period_filtered.replace(False, "Будни", inplace=True)
    df_period_filtered.replace(True, "Выходные", inplace=True)
    avg_expenses_grouped_by_dayoff = df_period_filtered.groupby(by="Дни").agg({'Сумма платежа': 'mean'})

    avg_expenses_grouped_by_dayoff['Сумма платежа'] = abs(avg_expenses_grouped_by_dayoff['Сумма платежа'])
    # result = {"Выходные": round(abs(avg_expenses_grouped_by_dayoff.loc[True].iloc[0]), 2),
    #           "Будни": round(abs(avg_expenses_grouped_by_dayoff.loc[False].iloc[0]), 2)}
    return avg_expenses_grouped_by_dayoff
