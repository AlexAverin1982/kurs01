import logging
import os
from datetime import datetime as datetime
from time import mktime, strptime

from pandas import DataFrame, Timestamp, read_excel, to_datetime

# ------------------------------------- настраиваем журналирование ------------------------------------------------

par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
utils_log_filename = os.path.join(par_dir, "logs", "utils.log")

# Основная конфигурация logging
logging.basicConfig(level=logging.INFO, filemode="w")
utils_logger = logging.getLogger("utils_logger")
utils_logger.setLevel(logging.INFO)
utils_log_handler = logging.FileHandler(filename=utils_log_filename, encoding="utf-8")

""" Формат записи логов включает метку времени, название модуля, уровень серьезности и сообщение """
utils_log_formatter = logging.Formatter("%(asctime)s %(levelname)s in module %(filename)s: %(message)s")
utils_log_handler.setFormatter(utils_log_formatter)
utils_logger.addHandler(utils_log_handler)


# ---------------------------------------------------------------------------------------------------------


def greet_user(current_time: datetime = datetime.now()):
    """Строка приветствия пользователя, различающаяся в зависимости от времени суток"""
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


def get_dataframe_from_xlsx(filepath: str) -> DataFrame:
    """Загружает данные по транзакциям из файлов excel"""
    try:
        df = read_excel(filepath)
        utils_logger.info(f"Данные из файла загружены успешно. Обнаружено {df.shape[0]} записей")
        return df
    except FileNotFoundError:
        utils_logger.error(f"Файл {filepath} не обнаружен")


def filter_operations_by_period(
    dataframe: DataFrame,
    period_column: str,
    period_start: datetime,
    period_end: datetime,
    expenses_column: str,
    filter_expenses: bool = True,
) -> DataFrame:
    """Фильтруем dataframe: берем только отчетный период и только траты (платеж меньше нуля)
    или только приход"""

    # convert date column into date format
    # report_date_start = datetime.strftime('%Y-%m-%d', strptime(period_start, date_format))
    # report_date_end = datetime.strftime('%Y-%m-%d', strptime(period_end, date_format))

    report_date_start = period_start
    report_date_end = period_end

    dataframe[period_column] = to_datetime(dataframe[period_column], dayfirst=True)

    df_period_filtered = dataframe[
        (dataframe[period_column] >= report_date_start) & (dataframe[period_column] <= report_date_end)
    ]
    utils_logger.info(f"Записи отфильтрованы за период с {str(report_date_start)} по {str(report_date_end)}")
    utils_logger.info(f"Обнаружено {df_period_filtered.shape[0]} записей")

    if filter_expenses:
        df_period_filtered = df_period_filtered[df_period_filtered[expenses_column] < 0]
        utils_logger.info("Записи содержат только данные о расходах")
        utils_logger.info(f"Обнаружено {df_period_filtered.shape[0]} записей")
    else:
        df_period_filtered = df_period_filtered[df_period_filtered[expenses_column] > 0]
        utils_logger.info("Записи содержат только данные о поступлениях")
        utils_logger.info(f"Обнаружено {df_period_filtered.shape[0]} записей")
        utils_logger.info("-" * 30)

    return df_period_filtered.sort_values(by=period_column)


def get_cards_totals(
    dataframe: DataFrame, card_no_column: str, payment_column: str, cashback_column: str
) -> list[dict]:
    """Сводные данные по картам: сумма трат и кэшбэка"""
    # группируем по номерам банковских карт
    df_grouped_by_cards = dataframe.groupby(by=card_no_column)
    utils_logger.info(f"Обнаружены записи по {df_grouped_by_cards.ngroups} картам ")
    utils_logger.info("-" * 30)
    agg_rule = {payment_column: "sum", cashback_column: "sum"}
    totals_by_cards = df_grouped_by_cards.agg(agg_rule)  # returns dataframe

    totals_by_cards.reset_index()  # make sure indexes pair with number of rows
    cards_data = []
    for card_no, row in totals_by_cards.iterrows():
        card_totals = {
            "last_digits": card_no[1:],
            "total_spent": round(float(abs(row[payment_column])), 2),
            "cashback": round(float(row[cashback_column]), 2),
        }
        cards_data.append(card_totals)

    return cards_data


def get_top_transactions(
    dataframe: DataFrame,
    transactions_count: int,
    payment_column: str,
    period_column: str,
    date_format: str,
    category_column: str,
    description_column: str,
) -> list[dict]:
    """Топ транзакций"""
    # сортируем исходные траты по убыванию
    transactions_top = dataframe[payment_column].nsmallest(transactions_count)
    utils_logger.info(
        f"Анализируем {dataframe.shape[0]} записей для поиска {transactions_count} самых крупных транзакций "
    )
    top_transactions = []
    for row_index in transactions_top.index:
        row = dataframe.loc[row_index]
        transaction = {
            "date": row[period_column].strftime(date_format),
            "amount": round(float(abs(row[payment_column])), 2),
            # "amount": "%.02f" % float(-row[payment_column]),
            "category": row[category_column],
            "description": row[description_column],
        }
        top_transactions.append(transaction)
    utils_logger.info(f"Сформировано {len(top_transactions)} записей")
    utils_logger.info("-" * 30)
    return top_transactions


def get_operations_totals(dataframe: DataFrame, payment_column: str) -> float:
    """Сводные данные: сумма трат"""
    totals = dataframe.agg({payment_column: "sum"})  # returns dataframe
    return float(abs(totals.iloc[0]))


def get_top_operations(
    dataframe: DataFrame, payment_column: str, category_column: str, categories_count: int = 0
) -> tuple[int, list[dict]]:
    """Топ расходов по категориям"""
    # группируем по категориям, суммируя расходы
    utils_logger.info(
        f"Анализируем {dataframe.shape[0]} записей для поиска {categories_count} самых затратных категорий "
    )

    agg_expenses_grouped_by_category = dataframe.groupby(by=category_column).agg({payment_column: "sum"})
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

    utils_logger.info(f"Общий расход: {total_expenses} по {len(top_expenses)} категориям")
    utils_logger.info("-" * 30)
    return total_expenses, top_expenses


def convert_dataframe_to_listdict(df: DataFrame) -> list[dict]:
    """Преобразует датафрейм в список словарей (не знаю, зачем)"""
    result = []
    fields = list(df.head(0).columns.values)
    for i in range(df.shape[0]):
        row = list(df.iloc[i])
        result.append(dict(zip(fields, row)))
    return result


def convert_values_in_listdict(
    listdict: list[dict], key_name: str, convert_to_type: type, format_str: str = ""
) -> None:
    """Преобразует значение укзаанного поля всех словарей списка к указанному типу"""

    for d in listdict:
        src_value = d.get(key_name)
        if not src_value:
            continue
        if convert_to_type is datetime:
            if isinstance(src_value, str):
                d[key_name] = datetime.strptime(src_value, format_str)
            elif isinstance(src_value, Timestamp):
                try:
                    d[key_name] = datetime.fromtimestamp(mktime(strptime(str(src_value), format_str)))
                except ValueError:
                    format_str = '%Y-%m-%d %H:%M:%S'
                    d[key_name] = datetime.fromtimestamp(mktime(strptime(str(src_value), format_str)))
        else:
            d[key_name] = convert_to_type(src_value)
