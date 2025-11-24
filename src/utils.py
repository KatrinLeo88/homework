import json
import os

from src.logger import setup_logger

logger = setup_logger("utils", "utils.log")


def load_json_list(path_to_file: str) -> list[dict | None]:
    """загружает список финансовых транзакци из JSON - файла"""
    logger.debug("Начало загрузки Json файла в path_to_file=%s", path_to_file)
    if not os.path.exists(path_to_file) or os.path.getsize(path_to_file) == 0:
        logger.error("Файл не найден или пустой, путь: path_to_file=%s", path_to_file)
        return []
    try:
        with open(path_to_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.debug("Файл успешно прочитан")
                return data
            else:
                return []
    except json.JSONDecodeError:
        return []
