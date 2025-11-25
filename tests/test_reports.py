import pytest

from src.reports import count_by_category, filter_by_query


@pytest.fixture
def transactions():
    return [
        {"description": "Перевод организации", "amount": 1000},
        {"description": "Перевод с карты на карту", "amount": 200},
        {"description": "Оплата товаров", "amount": 300},
        {"description": "Открытие вклада", "amount": 400},
    ]


def test_filter_by_query_found(transactions) -> None:
    result = filter_by_query(transactions, "Перевод")
    assert len(result) == 2
    assert result[0]["description"] == "Перевод организации"


def test_filter_by_query_not_found(transactions) -> None:
    result = filter_by_query(transactions, "Зарплата")
    assert len(result) == 0


def test_filter_by_query_empty_string(transactions) -> None:
    result = filter_by_query(transactions, "")
    assert result == []


def test_count_by_category(transactions) -> None:
    categories = ["Перевод", "Оплата", "Вклад"]
    result = count_by_category(transactions, categories)
    assert result["Перевод"] == 2
    assert result["Оплата"] == 1
    assert "Открытие" not in result  # Категория "Вклад" есть в "Открытие вклада"


def test_count_by_category_empty(transactions) -> None:
    result = count_by_category(transactions, [])
    assert result == {}
