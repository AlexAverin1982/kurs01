import os
import pytest

from src.decorators import log

par_dir = os.path.abspath(os.path.join(__file__, os.pardir))
par_dir = os.path.abspath(os.path.join(par_dir, os.pardir))
log_filename = os.path.join(par_dir, "logs", "decorator.log")


@log()
def logged_report_to_default_log_file() -> str:
    return ""


@log(log_filename)
def logged_report_to_default_log_file() -> str:
    return ""


def test_log_decorator_1(capsys: pytest.CaptureFixture) -> None:
    result = logged_report_to_default_log_file()
    captured = capsys.readouterr()
    assert (
        (result == "1234 56** **** 3456")
        and (captured[0].find(" ok\n") > 0)
        and (captured[0].find("\nResult is") > 0)
    )


