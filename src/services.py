from datetime import datetime as datetime
from typing import Any

from src.datetime_utils import get_month_dates
from src.utils import convert_values_in_listdict


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int) -> float:
    def get_savings(operation: dict) -> float:
        """Сумма, откладываемая в копилку"""
        expense_amount = operation.get("Сумма операции")
        expense_amount = abs(float(expense_amount))
        fract = 1 - (expense_amount - int(expense_amount))
        expense_amount = int(expense_amount)
        return limit - (expense_amount % limit) + fract - 1

        """ Вычисление остатка для накопления из словаря с данными о расходе"""
    """ Инвесткопилка. Позволяет копить через округление ваших трат.
        Можно задать комфортный порог округления: 10, 50 или 100 ₽. Траты будут округляться,
        и разница между фактической суммой трат по карте и суммой округления будет попадать на счет «Инвесткопилки».

    :param month: — месяц, для которого рассчитывается отложенная сумма (строка в формате 'YYYY-MM').
    :param transactions: — список словарей, содержащий информацию о транзакциях, в которых содержатся следующие поля:
            Дата операции — дата, когда произошла транзакция (строка в формате 'YYYY-MM-DD').
            Сумма операции — сумма транзакции в оригинальной валюте (число).
    :param limit: — предел, до которого нужно округлять суммы операций (целое число).
    :return: сумма, которую можно было бы накопить за указанный период при указанном округлении
    """

    date_start, date_end = get_month_dates(month)
    convert_values_in_listdict(transactions, "Дата операции", datetime, "%d.%m.%Y %H:%M:%S")
    # фильтруем расходы за период
    filtered_by_period = list(filter(lambda x: x.get("Дата операции") >= date_start, transactions))
    filtered_by_period = list(filter(lambda x: x.get("Дата операции") <= date_end, filtered_by_period))
    filtered_expenses = list(filter(lambda x: x.get("Сумма операции") < 0, filtered_by_period))

    savings = list(map(get_savings, filtered_expenses))

    return round(sum(savings), 2)
