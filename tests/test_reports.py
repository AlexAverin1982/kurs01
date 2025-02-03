import os

from src.reports import spending_by_workday
from src.utils import get_dataframe_from_xlsx


def test_spending_by_workday() -> None:
    """
    тестим spending_by_workday(transactions: DataFrame, date: Optional[str] = None) -> DataFrame:
    грузим тестовый датафрейм с тратами
    проверяем как он считает средние траты и как фильтрует диапазон

    """
    period_end = "2024-12-29 23:00:00"
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations report test.xlsx")
    dataframe = get_dataframe_from_xlsx(filename)
    result = spending_by_workday(dataframe, str(period_end))
    # поскольку тестировать датафреймы не умеем, выгружаем  итоговые данные в словарь,
    # будем сравнивать с ожидаемыми значениями
    result_dict = {col: int(row.iloc[0]) for col, row in result.iterrows()}

    expected_result_dict = {"Будни": 1000, "Выходные": 500}

    assert result_dict == expected_result_dict
