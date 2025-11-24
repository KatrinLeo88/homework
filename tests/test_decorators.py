from pathlib import Path
from typing import NoReturn

import pytest

from src.decorators import log


@log()
def add(x: int, y: int) -> int:
    return x + y


@log()
def divide(x: int, y: int) -> float:
    return x / y


@log(filename="test_log.txt")
def multiply(x: int, y: int) -> int:
    return x * y


def test_successful_function_console_log(capsys: pytest.CaptureFixture[str]) -> None:
    result = add(2, 3)
    assert result == 5
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_exception_function_console_log(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0), {}" in captured.out


def test_log_to_file(tmp_path: Path) -> None:
    test_file = tmp_path / "file_log.txt"

    @log(filename=str(test_file))
    def subtract(x: int, y: int) -> int:
        return x - y

    result = subtract(5, 3)
    assert result == 2

    with open(test_file, "r") as f:
        content = f.read()
    assert "subtract ok" in content


def test_error_log_to_file(tmp_path: Path) -> None:
    test_file = tmp_path / "file_log.txt"

    @log(filename=str(test_file))
    def divide_by_zero(_: int) -> NoReturn:
        raise ZeroDivisionError("division by zero")

    with pytest.raises(ZeroDivisionError):
        divide_by_zero(10)

    with open(test_file, "r") as f:
        content = f.read()
    assert "divide_by_zero error: ZeroDivisionError" in content
    assert "Inputs: (10,), {}" in content
