from datetime import datetime as datetime

from src.utils import show_main_page_menu, set_users_currencies
from src.views import show_main_page


def main():
    """ Точка входа приложения """
    while True:
        user_choice = show_main_page_menu()
        if user_choice == 99:
            break
        elif user_choice == 1:
            response = show_main_page()
            print(response)
        elif user_choice == 2:
            user_currencies = set_users_currencies()
            print('\n')
            for code, rate in user_currencies.items():
                print(f"1 {code} == {round(rate, 2)} руб.")
            print('\n')

if __name__ == "__main__":
    main()
