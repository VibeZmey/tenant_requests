"""Загрузка и сохранение данных в JSON."""
import json
import os
from datetime import date
from typing import List

from models import Request, Tenant, Executor
from models.tenants import add_tenant  # noqa: F401 (оставлено для совместимости)
from models.executors import add_executor  # noqa: F401

DATA_DIR = "data"


def load_raw(filename: str) -> list:
    """Загрузить JSON-файл как список словарей."""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Ошибка чтения файла {filename}. Данные повреждены.")
        return []


def save_raw(filename: str, data: list) -> None:
    """Сохранить список словарей в JSON-файл."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_tenants(filename: str = "tenants.json") -> List[Tenant]:
    """Загрузить коллекцию объектов Tenant."""
    return [Tenant.from_data(item) for item in load_raw(filename)]


def save_tenants(tenants: List[Tenant],
                 filename: str = "tenants.json") -> None:
    """Сохранить коллекцию объектов Tenant."""
    save_raw(filename, [t.to_data() for t in tenants])


def load_executors(filename: str = "executors.json") -> List[Executor]:
    """Загрузить коллекцию объектов Executor."""
    return [Executor.from_data(item) for item in load_raw(filename)]


def save_executors(executors: List[Executor],
                   filename: str = "executors.json") -> None:
    """Сохранить коллекцию объектов Executor."""
    save_raw(filename, [e.to_data() for e in executors])


def load_requests(
    tenants: List[Tenant],
    executors: List[Executor],
    filename: str = "requests.json",
) -> List[Request]:
    """Загрузить заявки, восстановив связи с жильцами и исполнителями."""
    requests: List[Request] = []
    for item in load_raw(filename):
        request = Request.from_data(item, tenants, executors)
        if request is not None:
            requests.append(request)
    return requests


def save_requests(requests: List[Request],
                  filename: str = "requests.json") -> None:
    """Сохранить коллекцию объектов Request."""
    save_raw(filename, [r.to_data() for r in requests])