import logging
import os
from datetime import datetime as datetime
from typing import Optional

from pandas import DataFrame

from src.decorators import log
from src.utils import filter_operations_by_period

par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
log_filename = os.path.join(par_dir, "logs", "log1.log")
# ------------------------------------- настраиваем журналирование ------------------------------------------------

report_log_filename = os.path.join(par_dir, "logs", "report.log")

# Основная конфигурация logging
logging.basicConfig(level=logging.INFO, filemode="w")
report_logger = logging.getLogger("report_logger")
report_logger.setLevel(logging.INFO)
report_log_handler = logging.FileHandler(filename=report_log_filename, encoding="utf-8")

""" Формат записи логов включает метку времени, название модуля, уровень серьезности и сообщение """
report_log_formatter = logging.Formatter("%(asctime)s %(levelname)s in module %(filename)s: %(message)s")
report_log_handler.setFormatter(report_log_formatter)
report_logger.addHandler(report_log_handler)


# ---------------------------------------------------------------------------------------------------------


@log(log_filename)
def spending_by_workday(transactions: DataFrame, date: Optional[str] = None) -> DataFrame:
    """
    :param transactions: датафрейм с транзакциями.
    :param date: Опциональная дата. Если дата не передана, то берется текущая дата.
    :return: Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты).
    """
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    report_logger.info(f"Анализируем {len(transactions)} записей.")
    # формируем даты трехмесячного периода
    date_start = date_end = date  # + tdelta(days=1) - tdelta(seconds=1)
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
            date_start = datetime(year, month, day, date_end.hour, date_end.minute, date_end.second)
            valid_date = True
        except ValueError:
            day -= 1
    # фильтруем датафрейм по периоду
    report_logger.info(f"фильтруем расходы за период с {str(date_start)} по {str(date_end)}")
    df_period_filtered = filter_operations_by_period(
        dataframe=transactions,
        period_column="Дата платежа",
        period_start=date_start,
        period_end=date_end,
        # date_format=date_format,
        expenses_column="Сумма платежа",
    )
    report_logger.info(f"Анализируем {df_period_filtered.shape[0]} записей по расходам за период.")
    # добавляем столбец с признаком выходного дня даты платежа
    df_period_filtered.insert(loc=0, column="Дни", value="")
    # df_period_filtered["Выходной"] = datetime.weekday(df_period_filtered['Дата платежа'])
    df_period_filtered["Дни"] = (df_period_filtered["Дата платежа"].apply(datetime.weekday) == 5) | (
        df_period_filtered["Дата платежа"].apply(datetime.weekday) == 6
    )
    # вычисляем средние траты по выходным и по будням

    df_period_filtered.replace(False, "Будни", inplace=True)
    df_period_filtered.replace(True, "Выходные", inplace=True)
    avg_expenses_grouped_by_dayoff = df_period_filtered.groupby(by="Дни").agg({"Сумма платежа": "mean"})

    avg_expenses_grouped_by_dayoff["Сумма платежа"] = abs(avg_expenses_grouped_by_dayoff["Сумма платежа"])
    # result = {"Выходные": round(abs(avg_expenses_grouped_by_dayoff.loc[True].iloc[0]), 2),
    #           "Будни": round(abs(avg_expenses_grouped_by_dayoff.loc[False].iloc[0]), 2)}
    report_logger.info(
        "По выходным за указанные 3 месяца в среднем тратилось "
        + f"{round(avg_expenses_grouped_by_dayoff.values[0][0], 2)} руб."
    )
    report_logger.info(
        "По будням за указанные 3 месяца в среднем тратилось "
        + f"{round(avg_expenses_grouped_by_dayoff.values[1][0], 2)} руб."
    )
    report_logger.info("-" * 30)
    return avg_expenses_grouped_by_dayoff
