import os
import tempfile

import pandas as pd
import pytest

from src.excel_parser import parse_csv, parse_excel

TEST_DATA = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2023-01-01T10:00:00Z",
        "amount": 1000,
        "currency_name": "Peso",
        "currency_code": "ARS",
        "from": "Account A",
        "to": "Account B",
        "description": "Test transaction",
    }
]


@pytest.fixture
def csv_file() -> None:
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", newline="", delete=False) as f:
        df = pd.DataFrame(TEST_DATA)
        df.to_csv(f.name, sep=";", index=False)
        yield f.name
    os.remove(f.name)


@pytest.fixture
def excel_file() -> None:
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
        df = pd.DataFrame(TEST_DATA)
        df.to_excel(f.name, index=False)
        yield f.name
    os.remove(f.name)


def test_read_csv_transactions(csv_file) -> None:
    result = parse_csv(csv_file)

    assert isinstance(result, list)
    assert result[0]["id"] == 1
    assert result[0]["amount"] == 1000
    assert result[0]["description"] == "Test transaction"


def test_read_excel_transactions(excel_file) -> None:
    result = parse_excel(excel_file)
    assert isinstance(result, list)
    assert result[0]["id"] == 1
    assert result[0]["amount"] == 1000
    assert result[0]["description"] == "Test transaction"
