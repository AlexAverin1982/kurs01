from datetime import datetime as datetime

from src.views import show_main_page


def main():
    """ Точка входа приложения """
    response = show_main_page()


if __name__ == "__main__":
    main()
