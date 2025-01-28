from datetime import datetime as datetime

from src.menus import show_main_page_menu
from src.currencies_and_stocks_utils import select_users_currencies, show_users_rates, cache_stocks, cache_currencies, \
    convert_stocks_prices
from src.views import show_main_page, show_events_page


def main():
    """ Точка входа приложения """
    cache_currencies()
    cache_stocks()

    while True:
        user_choice = show_main_page_menu()
        if user_choice == 99:
            break
        elif user_choice == 1:                  # статистика по банковским операциям
            response = show_main_page()
            print(response)
        elif user_choice == 2:                          # валюты и акции
            user_currencies = select_users_currencies()
            show_users_rates(user_currencies)
        elif user_choice == 3:                           # страница события: статистика по тратам и приходам
            response = show_events_page()
            print(response)


if __name__ == "__main__":
    main()
