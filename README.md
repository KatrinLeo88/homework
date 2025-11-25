# Учебный проект

Этот поект необходим для того, чтобы я научилась программировать.

## Стек технологий

- Python 3.13
- flake8
- mypy
- black

## Установка и запуск

1. **Клонировать репозиторий:**
```bash
git clone git@github.com:katrinleo/homework.git
cd PythonProject13
```

2. **Создать и активировать виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# или
venv\Scripts\activate  # Windows
```

3. **Установить зависимости:**
```bash
poetry install
```
4. **Активировать виртуальное окружение Poetry:**
```bash
poetry shell
```
5. **создан модуль generators.py, 
содержащий функции для работы с массивами транзакций.**
6. **создан модуль excel_parser.py, содержащий функции для работы с таблицами.**
7. **создан модуль reports.py для поиска транзакций (re) и подсчета категорий.**
8. **создан модуль main.py с консольным интерфейсом для пользователя.**