import json
import os

DATA_DIR = "data"


def load_data(filename: str) -> list:
    """Загрузка данных из JSON файла."""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Ошибка чтения файла {filename}. Данные повреждены.")
        return []


def save_data(filename: str, data: list) -> None:
    """Сохранение данных в JSON файл."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)