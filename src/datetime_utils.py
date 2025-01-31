from datetime import datetime as datetime
from datetime import timedelta as tdelta
from time import mktime, strptime


def is_leap_year(year: int) -> bool:
    """Проверка года на високосность"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def get_date(
    format_string: str = "%d.%m.%Y", prompt: str = "Введите дату конца отчетного периода: ", show_format: bool = True
) -> datetime:
    """Запрашиваем у пользователя дату из отчетного периода"""

    correct_input = False
    period_end = datetime.now()
    while not correct_input:
        try:
            if show_format:
                print(f"Корректный формат ввода даты: {format_string}\n")
            period_end = input(prompt)
            period_end = datetime.strptime(period_end, format_string)
            correct_input = True
        except ValueError:
            print("Неверный формат ввода даты.\n")
    return period_end


def get_period(
    date_format: str = "YYYY-MM-DD HH:MM:SS", prompt: str = "Введите дату конца отчетного периода: "
) -> tuple[datetime, datetime]:
    """Запрашиваем у пользователя дату из отчетного периода
    и возвращаем начало месяца и введенную дату того же месяца"""

    # переводим отображаемую маску даты в приемлемую для функции
    format_string = date_format.replace("YYYY", "%Y").replace("MM", "%m", 1).replace("DD", "%d")
    format_string = format_string.replace("HH", "%H").replace("MM", "%M").replace("SS", "%S")
    print(f"Корректный формат ввода даты: {date_format}\n")
    period_end = get_date(format_string, prompt, show_format=False)
    period_start = datetime(period_end.year, period_end.month, 1)
    return period_start, period_end


def get_report_span() -> str:
    """Выбор кода периода"""
    print("\nВведите длительность отчетного периода:")
    print("W — неделя, на которую приходится дата;")
    print("M — месяц, на который приходится дата;")
    print("Y — год, на который приходится дата;")
    print("ALL — все данные до указанной даты.")
    print("Любая другая строка - период по умолчанию = месяц указанной даты")
    return input().upper()


def get_span_dates(report_date: datetime, report_span: str) -> tuple[datetime, datetime]:
    """Возвращает первую и последнюю даты периодов: недели, месяца, года"""
    date_start = date_end = report_date
    if report_span == "W":  # неделя
        while date_start.weekday():
            date_start = date_start - tdelta(days=1)
        while date_end.weekday() < 6:
            date_end = date_end + tdelta(days=1)
        date_end = date_end + tdelta(days=1) - tdelta(seconds=1)
    elif report_span == "ALL":  # с начала прошлого века и до конца текущего дня
        date_start = datetime(1900, 1, 1)
        date_end = date_end + tdelta(days=1) - tdelta(seconds=1)
    elif report_span == "Y":  # текущий год
        date_start = datetime(date_start.year, 1, 1)
        date_end = date_start + tdelta(days=365 + int(is_leap_year(date_start.year))) - tdelta(seconds=1)
    else:  # текущий месяц
        date_start = datetime(date_start.year, date_start.month, 1)
        date_end = datetime(date_start.year, date_start.month, 28)

        while date_start.month == date_end.month:
            date_end = date_end + tdelta(days=1)
        date_end = date_end - tdelta(seconds=1)
    return date_start, date_end


def get_month_dates(year_month_date_part: str) -> tuple[datetime, datetime]:
    """Функция возвращает первую и последнюю даты месяца, указанного во формате YYYY-MM"""
    s = year_month_date_part + "-01"
    date_start = datetime.strptime(year_month_date_part + "-01", "%Y-%m-%d")
    date_end = date_start + tdelta(days=27)
    while date_start.month == date_end.month:
        date_end = date_end + tdelta(days=1)
    date_end = date_end - tdelta(seconds=1)
    return date_start, date_end
