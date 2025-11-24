import json
import os

import pytest

from src.utils import load_json_list


@pytest.fixture
def temp_json_file(tmp_path):
    data = [
        {"id": 1, "operationAmount": {"amount": "1000.00", "currency": {"code": "RUB", "name": "руб."}}},
        {"id": 2, "operationAmount": {"amount": "200.00", "currency": {"code": "USD", "name": "доллары"}}},
    ]
    file_path = tmp_path / "operations.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return file_path


def test_load_json_list_valid(temp_json_file) -> None:
    result = load_json_list(str(temp_json_file))
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["operationAmount"]["currency"]["code"] == "USD"


def test_load_json_list_empty_file(tmp_path) -> None:
    file_path = tmp_path / "empty.json"
    file_path.write_text("")
    result = load_json_list(str(file_path))
    assert result == []


def test_load_json_list_file_not_found() -> None:
    result = load_json_list("nonexistent_file.json")
    assert result == []


def test_load_real_operations() -> None:
    result = load_json_list("data/operations.json")
    assert isinstance(result, list)
    assert all(isinstance(txn, dict) for txn in result)
