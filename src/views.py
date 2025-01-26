from src.utils import get_period, greet_user, get_dataframe_from_xlsx, load_ops_from_xlsx
from json import dumps
import os.path


def show_main_page() -> str:
    result = {'greeting': greet_user()}
    par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
    par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
    filename = os.path.join(par_dir, "data", "operations.xlsx")

    dataframe = get_dataframe_from_xlsx(filename)

    op_data = load_ops_from_xlsx(filename)
    stats = {}
    for item in op_data:
        payment_sum = float(item.get('Сумма платежа', 0))
        if payment_sum >= 0:
            continue

        card_number = item.get('Номер карты', '')
        if not card_number:
            continue
        totals = stats.get(card_number)

        if totals:
            balance = totals.get('balance')
            if balance:
                totals['balance'] = balance + payment_sum
        else:
            totals = {'balance': payment_sum}

        cashback = float(item.get('Кэшбэк', 0))

        total_cashback = totals.get('cashback', 0)
        totals['cashback'] = total_cashback + cashback
        stats[card_number] = totals

    # группируем по номерам банковских карт
    cards = dataframe.groupby(by='Номер карты', as_index=True)

    # card_numbers =

    cards_data = []
    for _, number in list(cards['Номер карты']):
        card_totals = {"last_digits": number[1:]}
        cards_data.append(card_totals)

    result['cards'] = cards_data

    report_period = get_period()
    return dumps(result)
