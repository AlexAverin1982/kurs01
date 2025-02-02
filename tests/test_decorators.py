import os

from src.decorators import log

par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
log_filename1 = os.path.join(par_dir, "logs", "log.log")
log_filename2 = os.path.join(par_dir, "logs", "test_log.log")


@log()
def logged_report_to_default_log_file() -> str:
    # логгером тестируется отчет
    return ""


@log(log_filename2)
def logged_report_to_log_with_filename() -> str:
    return ""


def test_log_decorator_1() -> None:
    """
    проверим наличие файла, куда будем писать,
    удаляем его, если он есть
    вызываем функцию с записью в этот файл
    проверяем, появился ли этот файл
    проверяем его содержимое
    """
    if os.path.exists(log_filename1):
        os.remove(log_filename1)

    logged_report_to_default_log_file()

    passed = os.path.exists(log_filename1)

    if passed:
        with open(log_filename1, "r") as f:
            lines = f.readlines()
            passed = len(lines) > 4
            passed = (
                (lines[0].startswith("logged_report_to_default_log_file() call start at "))
                and (lines[1].startswith("logged_report_to_default_log_file() ok"))
                and (lines[2].startswith("logged_report_to_default_log_file() finished at "))
                and (lines[3].startswith("Run time: 0.0"))
                and (lines[4].startswith("Result is"))
            )
    assert passed


def test_log_decorator_2() -> None:
    """
    проверим наличие файла, куда будем писать,
    удаляем его, если он есть
    вызываем функцию с записью в этот файл
    проверяем, появился ли этот файл
    проверяем его содержимое
    """
    if os.path.exists(log_filename2):
        os.remove(log_filename2)

    logged_report_to_log_with_filename()

    passed = os.path.exists(log_filename2)

    if passed:
        with open(log_filename2, "r") as f:
            lines = f.readlines()
            passed = len(lines) > 4
            passed = (
                (lines[0].startswith("logged_report_to_log_with_filename() call start at "))
                and (lines[1].startswith("logged_report_to_log_with_filename() ok"))
                and (lines[2].startswith("logged_report_to_log_with_filename() finished at "))
                and (lines[3].startswith("Run time: 0.0"))
                and (lines[4].startswith("Result is"))
            )
    assert passed
