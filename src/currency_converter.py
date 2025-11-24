import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
API_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(transaction: Dict) -> float:
    """Конвертирует сумму транзакции в рубли по текущему курсу"""

    amount = float(transaction["operationAmount"]["amount"])

    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return float(amount)
    try:
        response = requests.get(
            API_URL, params={"base": currency, "symbols": "RUB"}, headers={"apikey": API_KEY}, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        rate = data["rates"]["RUB"]
        return round(float(amount) * rate, 2)

    except (requests.RequestException, KeyError, TypeError) as e:
        raise RuntimeError("Ошибка при получении курса валют") from e
