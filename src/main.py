import src.currencies_and_stocks_utils
from src.currencies_and_stocks_utils import cache_currencies, cache_stocks
from src.menus import show_main_page_menu
from src.views import show_events_page, show_investment_page, show_main_page, show_reports_page


def main() -> None:
    """Точка входа приложения"""
    """ кэшируем данные по валютам и акциям сразу в начале работы приложения
    для ограничения количества обращений к апи впоследствии, обновляя кэш при необходимости"""
    cache_currencies(file_cache_is_enough=True)  # узнаем курсы валют и акций
    cache_stocks(file_cache_is_enough=True)

    while True:
        user_choice = show_main_page_menu()
        if user_choice == 9:
            break
        elif user_choice == 1:  # статистика по банковским операциям
            response = show_main_page()
            print(response)
        # elif user_choice == 2:  # валюты и акции
        #     user_currencies = select_users_currencies()
        #     show_users_rates(user_currencies)
        elif user_choice == 2:  # страница события: статистика по тратам и приходам
            response = show_events_page()
            print(response)
        elif user_choice == 3:  # страница сервисы: инвесткопилка
            response = show_investment_page()
            print(response)
        elif user_choice == 4:  # страница отчеты: Траты в рабочий/выходной день
            response = show_reports_page()
            print(response)
        elif user_choice == 5:  # страница отчеты: Траты в рабочий/выходной день
            src.currencies_and_stocks_utils.cache_currencies(file_cache_is_enough=False)
            src.currencies_and_stocks_utils.cache_stocks(file_cache_is_enough=False)
            print("Цены обновлены")


if __name__ == "__main__":
    main()
