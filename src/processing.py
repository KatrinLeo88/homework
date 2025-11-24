def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """функция принимающая список словарей и
    возвращающая отфильтрованный список словарей"""
    output_data = []
    for d in data:
        if d.get("state") == state:
            output_data.append(d)
    return output_data


def sort_by_date(data: list[dict], descending: bool = True) -> list[dict]:
    """функиия принимает список словарей и сортирует по дате"""
    return sorted(data, key=lambda x: x.get("date", ""), reverse=descending)
