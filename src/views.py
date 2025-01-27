from time import strptime, strftime
import datetime as dt
from datetime import datetime as datetime
from src.utils import get_period, greet_user, get_dataframe_from_xlsx, filter_expenses_by_period, \
    get_cards_totals, get_top_transactions, load_currencies_and_stocks_from_json
from json import dumps


import os.path


def show_main_page() -> str:
    """ JSON-данные для главной web-страницы """
    result = {'greeting': greet_user()}
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations.xlsx")

    dataframe = get_dataframe_from_xlsx(filename)

    # op_data = load_ops_from_xlsx(filename)

    report_date_start, report_date_end = get_period()
    # date_format = '%d.%m.%Y'
    date_format = 'YYYY-MM-DD HH:MM:SS'
    report_date_start = report_date_start.strftime(date_format)
    report_date_end = report_date_end.strftime(date_format)

    # report_date_start = '01.12.2021'
    # report_date_end = '19.12.2021'

    # фильтруем траты по периоду
    df_period_filtered = filter_expenses_by_period(dataframe=dataframe,
                                                   period_column='Дата платежа',
                                                   period_start=report_date_start,
                                                   period_end=report_date_end,
                                                   date_format=date_format,
                                                   expenses_column='Сумма платежа')

    # получаем сводные данные по картам
    result['cards'] = get_cards_totals(dataframe=df_period_filtered,
                                       card_no_column='Номер карты',
                                       payment_column='Сумма платежа',
                                       cashback_column='Кэшбэк')

    result['top_transactions'] = get_top_transactions(dataframe=df_period_filtered, transactions_count=5,
                                                      payment_column='Сумма платежа', period_column='Дата платежа',
                                                      date_format='%d.%m.%Y', category_column='Категория',
                                                      description_column='Описание')

    filename = os.path.join(par_dir, "user_settings.json")

    currencies_and_stocks = load_currencies_and_stocks_from_json(filename)

    result['currency_rates'] = get_currencies_rates(currencies_and_stocks)

    return dumps(result)
