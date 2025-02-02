import os

from src.services import investment_bank
from src.utils import convert_dataframe_to_listdict, get_dataframe_from_xlsx


def test_investment_bank() -> None:
    """
    тестим инвест копилку
    грузим тестовый датафрейм
    проверяем, как он считает, сколько можно сэкономить
    """
    month = "2024-12"
    limit = 50
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations report test.xlsx")
    dataframe = get_dataframe_from_xlsx(filename)
    transactions = convert_dataframe_to_listdict(dataframe)
    savings = investment_bank(month, transactions, limit)

    """
    в тестовых данных за указанный месяц семь трат кратных 100 и одна рубль
    """
    assert int(savings) == 7 * limit + (limit - 1)
