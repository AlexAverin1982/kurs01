import datetime as dt
from datetime import datetime as datetime
from time import strptime
from pandas import read_excel, DataFrame


def greet_user(time: datetime = datetime.now()):
    """ Строка приветствия пользователя, различающаяся в зависимости от времени суток """
    if time.hour * 60 + time.minute < 340:
        print("Доброй ночи")
    elif time.hour * 60 + time.minute < 12 * 60:
        print("Доброе утро")
    elif time.hour * 60 + time.minute < 17 * 60:
        print("Добрый день")
    elif time.hour * 60 + time.minute < 22 * 60:
        print("Добрый вечер")
    else:
        print("Доброй ночи")


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
    """загружает данные по транзакциям из файлов excel"""
    return read_excel(filepath)


def load_ops_from_xlsx(filepath: str) -> list[dict]:
    """загружает данные по транзакциям из файлов excel"""
    result = []
    try:
        # column_types = {'id': int, 'state': str, 'date': datetime, 'amount': int,
        #                 'currency_name': str, 'currency_code':str, 'from': str, 'to': str, 'description': str}
        excel_data = read_excel(filepath, dtype=str)
        fields = list(excel_data.head(0).columns.values)
        for i in range(excel_data.shape[0]):
            row = list(excel_data.iloc[i])
            result.append(dict(zip(fields, row)))
    except:
        result = []

    return result
