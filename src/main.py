import os

from src.excel_parser import parse_csv, parse_excel
from src.logger import setup_logger
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.reports import filter_by_query
from src.utils import load_json_list

logger = setup_logger("main", "main.log")

PATH_JSON = os.path.join("data", "operations.json")
PATH_CSV = os.path.join("data", "transactions.csv")
PATH_XLSX = os.path.join("data", "transactions_excel.xlsx")


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    user_input = input("Пользователь: ")
    transactions: list[dict] = []

    if user_input == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        transactions = load_json_list(PATH_JSON)
    elif user_input == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        transactions = parse_csv(PATH_CSV)
    elif user_input == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        transactions = parse_excel(PATH_XLSX)
    else:
        print("Программа: Некорректный ввод. Выбран JSON-файл по умолчанию.")
        transactions = load_json_list(PATH_JSON)

    while True:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input("Пользователь: ").upper().strip()

        if status in ["EXECUTED", "CANCELED", "PENDING"]:
            break
        print(f'Программа: Статус операции "{status}" недоступен.')

    filtered_by_state = filter_by_state(transactions, status)
    print(f'Программа: Операции отфильтрованы по статусу "{status}"')

    print("Программа: Отсортировать операции по дате? Да/Нет")
    sort_answer = input("Пользователь: ").lower().strip()

    if sort_answer == "да":
        print("Программа: Отсортировать по возрастанию или по убыванию?")
        order_answer = input("Пользователь: ").lower().strip()
        is_descending = order_answer == "по убыванию"
        filtered_by_state = sort_by_date(filtered_by_state, is_descending)

    print("Программа: Выводить только рублевые транзакции? Да/Нет")
    rub_answer = input("Пользователь: ").lower().strip()

    if rub_answer == "да":

        rub_transactions = []
        for t in filtered_by_state:
            code = "UNKNOWN"
            if "currency_code" in t:  # CSV/Excel
                code = t["currency_code"]
            elif "operationAmount" in t:  # JSON
                code = t["operationAmount"]["currency"]["code"]

            if code == "RUB":
                rub_transactions.append(t)
        filtered_by_state = rub_transactions

    print("Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    search_answer = input("Пользователь: ").lower().strip()

    if search_answer == "да":
        print("Программа: Введите слово для поиска:")
        search_word = input("Пользователь: ")
        filtered_by_state = filter_by_query(filtered_by_state, search_word)

    print("Программа: Распечатываю итоговый список транзакций...")

    if not filtered_by_state:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа: Всего банковских операций в выборке: {len(filtered_by_state)}")
    print()

    for t in filtered_by_state:
        date_str = t.get("date", "")
        if "T" in str(date_str):
            date_formatted = date_str.split("T")[0].split("-")
            date_output = f"{date_formatted[2]}.{date_formatted[1]}.{date_formatted[0]}"
        else:
            date_output = str(date_str)

        description = t.get("description", "")

        from_info = t.get("from")
        to_info = t.get("to")

        transfer_info = ""
        if from_info and to_info:
            masked_from = (
                get_mask_card_number(from_info) if "Счет" not in str(from_info) else get_mask_account(from_info)
            )
            masked_to = get_mask_card_number(to_info) if "Счет" not in str(to_info) else get_mask_account(to_info)
            transfer_info = f"{masked_from} -> {masked_to}"
        elif to_info:
            masked_to = get_mask_card_number(to_info) if "Счет" not in str(to_info) else get_mask_account(to_info)
            transfer_info = f"{masked_to}"

        amount = 0
        currency = ""
        if "amount" in t and isinstance(t["amount"], (int, float)) and "currency_name" in t:  # Excel/CSV
            amount = t["amount"]
            currency = t["currency_name"]
        elif "operationAmount" in t:  # JSON
            amount = t["operationAmount"]["amount"]
            currency = t["operationAmount"]["currency"]["name"]

        print(f"{date_output} {description}")
        if transfer_info:
            print(transfer_info)
        print(f"Сумма: {amount} {currency}")
        print()


if __name__ == "__main__":
    main()
