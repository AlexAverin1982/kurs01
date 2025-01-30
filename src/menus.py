def show_main_page_menu() -> int:
    while True:
        print("-" * 20 + " Главная страница " + "-" * 20)
        print("Выберите дальнейшее действие: ")
        print("1. Главная страница: статистика по банковским картам, валюты и акции")
        print("2. Информация о валютах и акциях")
        print('3. Страница "События": статистика по расходам и доходам')
        print('4. Страница "Сервисы": инвесткопилка')
        print('5. Страница "Отчеты": Средние траты в рабочий/выходной день за 3 месяца')
        print("9. Выход")
        user_input = input("\nВаш выбор: ")
        if user_input.isdigit():
            break
    return int(user_input)


def show_currencies_and_stocks_menu() -> int:
    while True:
        print("-" * 20 + " Валюты и акции " + "-" * 20)
        print("Выберите дальнейшее действие: ")
        print("1. Загрузить валюты и акции из файла JSON")
        print("2. Ввести валюты вручную")
        print("3. Ввести акции вручную")
        print("4. Информация о валютах и акциях")
        print("5. Сохранить валюты и акции в файл JSON")
        print("99. Выход")
        user_input = input("\nВаш выбор: ")
        if user_input.isdigit():
            break
    return int(user_input)
