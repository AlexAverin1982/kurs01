import logging
import os
from datetime import datetime as datetime
from typing import Any

from src.datetime_utils import get_month_dates
from src.utils import convert_values_in_listdict

# ------------------------------------- настраиваем журналирование ------------------------------------------------

par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
invest_log_filename = os.path.join(par_dir, "logs", "investments.log")

# Основная конфигурация logging
logging.basicConfig(level=logging.INFO, filemode="w")
invest_logger = logging.getLogger("invest_logger")
invest_logger.setLevel(logging.INFO)
invest_log_handler = logging.FileHandler(filename=invest_log_filename, encoding="utf-8")

""" Формат записи логов включает метку времени, название модуля, уровень серьезности и сообщение """
invest_log_formatter = logging.Formatter("%(asctime)s %(levelname)s in module %(filename)s: %(message)s")
invest_log_handler.setFormatter(invest_log_formatter)
invest_logger.addHandler(invest_log_handler)


# ---------------------------------------------------------------------------------------------------------


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int) -> float:
    """Вычисление остатка для накопления из словаря с данными о расходе"""

    def get_savings(operation: dict) -> float:
        """Сумма, откладываемая в копилку"""
        expense_amount = operation.get("Сумма операции")
        expense_amount = abs(float(expense_amount))
        fract = 1 - (expense_amount - int(expense_amount))
        expense_amount = int(expense_amount)
        saved = limit - (expense_amount % limit) + fract - 1
        invest_logger.info(f"С потраченной суммы {expense_amount} откладываем {round(saved, 2)} руб.")
        return saved

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
    invest_logger.info(f"Анализируем {len(transactions)} записей.")
    invest_logger.info(f"Порог округления: {limit} руб.")
    convert_values_in_listdict(transactions, "Дата операции", datetime, "%d.%m.%Y %H:%M:%S")
    # фильтруем расходы за период
    invest_logger.info(f"фильтруем расходы за период с {str(date_start)} по {str(date_end)}")
    filtered_by_period = list(filter(lambda x: x.get("Дата операции") >= date_start, transactions))
    filtered_by_period = list(filter(lambda x: x.get("Дата операции") <= date_end, filtered_by_period))
    filtered_expenses = list(filter(lambda x: x.get("Сумма операции") < 0, filtered_by_period))
    invest_logger.info(f"Анализируем {len(filtered_expenses)} записей по расходам.")
    savings = list(map(get_savings, filtered_expenses))

    result = round(sum(savings), 2)
    invest_logger.info(f"Всего отложили {result} руб.")
    invest_logger.info("-" * 30)
    return result
