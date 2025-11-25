from unittest.mock import patch

import pytest

from src.currency_converter import convert_to_rub


@patch("src.currency_converter.requests.get")
@pytest.mark.parametrize(
    "transaction, rate, expected_result",
    [
        ({"operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "доллары"}}}, 90.0, 9000.0),
        ({"operationAmount": {"amount": "50.50", "currency": {"code": "EUR", "name": "евро"}}}, 98.5, 4974.25),
    ],
)
def test_convert_foreign_currency(mock_get, transaction, rate, expected_result) -> None:
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"RUB": rate}}
    result = convert_to_rub(transaction)
    assert result == expected_result


def test_convert_rub_currency() -> None:
    transaction = {"operationAmount": {"amount": "1234.56", "currency": {"code": "RUB", "name": "руб."}}}
    result = convert_to_rub(transaction)
    assert result == 1234.56
