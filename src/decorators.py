import os
from functools import wraps
from time import ctime, time
from typing import Any, Callable


def log(filename: str = "") -> Callable:  # декоратор для журналирования работы функций
    """Декоратор журналирования работы функций с выводом информации в файл или консоль"""

    # внешний декоратор - принимает параметры работы декоратора
    def wrapper(func: Callable) -> Callable:
        # замыкание - возврат обернутой функции вместо исходной
        @wraps(func)  # сохраняем справочную информацию по декорируемой функции и ее имя
        def inner(*args: Any, **kwargs: Any) -> Any:
            # процесс обертывания функции в журналирование
            log = []
            result = None
            try:
                time_start = time()
                log.append(f"{func.__name__}() call start at {ctime(time_start)}")
                result = func(*args, **kwargs)
                time_end = time()
                log.append(f"{func.__name__}() ok")
                log.append(f"{func.__name__}() finished at {ctime(time_end)}")
                log.append(f"Run time: {time_end - time_start}")
                log.append(f"Result is {result}")
            except Exception as e:  # фиксируем информацию по исключению
                args_line = ""
                if args:  # фиксируем список значений аргументов
                    for arg in args:
                        args_line = args_line + "," + str(arg)
                if kwargs:
                    for arg in kwargs:
                        args_line = args_line + "," + str(arg)
                while args_line and args_line[0] == ",":
                    args_line = args_line[1:].strip()

                log.append(f"{func.__name__}() error: {e}. Inputs: {args_line}")

            nonlocal filename
            if not filename:  # имя файла по умолчанию
                par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
                par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
                filename = os.path.join(par_dir, "logs", "log.log")

            with open(filename, "a", encoding="utf-8") as f:
                for line in log:
                    f.write(line + "\n")
            return result

        return inner

    return wrapper
