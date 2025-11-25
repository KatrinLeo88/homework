import re
from collections import Counter

from src.logger import setup_logger

logger = setup_logger("reports", "reports.log")


def filter_by_query(transactions: list[dict], query: str) -> list[dict]:
    """
    Функция принимает список словарей с данными о банковских операциях и строку поиска,
    а возвращает список словарей, у которых в описании есть данная строка.
    """
    logger.debug(f"Запуск поиска по запросу: {query}")
    if not query:
        return []

    pattern = re.compile(query, re.IGNORECASE)
    result = []

    for transaction in transactions:
        description = str(transaction.get("description", ""))
        if pattern.search(description):
            result.append(transaction)

    logger.debug(f"Найдено {len(result)} записей")
    return result


def count_by_category(transactions: list[dict], categories: list[str]) -> dict[str, int]:
    """
    Функция принимает список словарей и список категорий операций,
    а возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории.
    """
    logger.debug("Запуск подсчета по категориям")
    if not categories:
        return {}

    found_categories = []

    for transaction in transactions:
        description = str(transaction.get("description", "")).lower()
        for category in categories:
            if category.lower() in description:
                found_categories.append(category)

    result = dict(Counter(found_categories))
    logger.debug(f"Результат подсчета: {result}")
    return result
