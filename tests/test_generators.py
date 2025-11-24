from typing import Iterator

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture()
def transactions() -> list[dict]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]


def test_filter_by_currency(transactions: list[dict]) -> None:
    usd_transactions = filter_by_currency(transactions, "USD")
    assert isinstance(usd_transactions, Iterator)
    assert list(usd_transactions) == transactions


def test_transaction_descriptions(transactions: list[dict]) -> None:
    descriptions = transaction_descriptions(transactions)
    for _ in range(2):
        assert isinstance(next(descriptions), str)


@pytest.mark.parametrize(
    "start, stop",
    [
        (1, 15),
        (9999999999999990, 9999999999999999),
    ],
)
def test_card_number_generator(start: int, stop: int) -> None:
    card_numbers = card_number_generator(start, stop)
    for _ in range(9):
        assert isinstance(next(card_numbers), str)
