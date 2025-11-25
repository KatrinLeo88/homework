import pandas as pd


def parse_csv(path: str) -> list[dict]:
    """функция читает csv фаил и возвращает список транзакции"""
    df = pd.read_csv(path, delimiter=";")
    transactions = df.to_dict(orient="records")

    return transactions


def parse_excel(path: str) -> list[dict]:
    """функция читает exel файл и возвращает список транзакции"""
    df = pd.read_excel(path)
    transactions = df.to_dict(orient="records")

    return transactions
