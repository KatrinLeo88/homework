import random

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def get_card() -> str:
    data = [
        "Maestro 1596837868705199",
        "MasterCard 7158300734726758",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
    ]

    return random.choice(data)


def test_get_mask_card_number(get_card: str) -> None:
    """тест функции get_mask_card_number"""
    result = get_mask_card_number(get_card)

    assert result[-4:].isdigit()
    assert result[:4].isalpha()


@pytest.mark.parametrize(
    "account",
    [
        "Счет 73654108430135874305",
        "Счет 35383033474447895560",
        "Счет 64686473678894779589",
    ],
)
def test_get_mask_account(account: str) -> None:
    """тест функции get_mask_account"""
    result = get_mask_account(account)
    assert len(result) < len(account)
    assert result[-4:].isdigit()
